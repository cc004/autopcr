import asyncio
import base64
import hashlib
import pickle
from collections import OrderedDict
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw
from dataclasses_json import dataclass_json

from ..constants import CACHE_DIR
from ..db.imagemgr import instance as imagemgr

@dataclass_json
@dataclass
class UnitCell:
    hist: np.ndarray
    template: np.ndarray
    arr_hash: np.ndarray
    md5: str

class UnitRecognizer:
    _instance = None
    _ROI_Y = (25, 96)
    _ROI_X = (8, 97)
    _HIST_BINS = [30, 32]
    _HIST_RANGE = [0, 180, 0, 256]
    _TEMPLATE_SCALES = (1.0, 0.9, 1.1)
    _CV_HIST_TOP_N = 30

    def __init__(self):
        self.data_path = Path(CACHE_DIR) / 'unit_recognizer.pkl'
        self._templates: Dict[int, UnitCell] = {}
        self._uid_arr: np.ndarray = np.empty((0,), dtype=np.int32)
        self._hash_arr: np.ndarray = np.empty((0, 0), dtype=np.uint8)
        self._hist_centered_arr: np.ndarray = np.empty((0, 0), dtype=np.float32)
        self._hist_norm_arr: np.ndarray = np.empty((0,), dtype=np.float32)
        self._template_scaled_cache: Dict[int, List[np.ndarray]] = {}
        self._unit_result_cache: OrderedDict[bytes, Tuple[int, int]] = OrderedDict()
        self._unit_result_cache_max = 4096
        self.init = False
        self.ver = None
        self._lock = asyncio.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _compute_hash(self, image: Image.Image, hash_size=16) -> np.ndarray:
        """
        计算图像的差异哈希 (dHash)。
        resize成 (hash_size + 1, hash_size)，比较每行相邻像素。
        """
        gray = np.asarray(
            image.resize((hash_size + 1, hash_size), Image.Resampling.BILINEAR).convert('L'),
            dtype=np.uint8
        )
        return (gray[:, :-1] > gray[:, 1:]).astype(np.uint8).reshape(-1)

    @staticmethod
    def _topk_indices(values: np.ndarray, k: int, largest: bool) -> np.ndarray:
        n = values.shape[0]
        if n <= 0 or k <= 0:
            return np.empty((0,), dtype=np.int32)
        k = min(k, n)
        if k == n:
            order = np.argsort(values)
            if largest:
                order = order[::-1]
            return order.astype(np.int32)

        if largest:
            part = np.argpartition(values, n - k)[n - k:]
            order = np.argsort(values[part])[::-1]
        else:
            part = np.argpartition(values, k - 1)[:k]
            order = np.argsort(values[part])
        return part[order].astype(np.int32)

    @classmethod
    def _extract_roi(cls, img_arr: np.ndarray) -> np.ndarray:
        y1, y2 = cls._ROI_Y
        x1, x2 = cls._ROI_X
        return img_arr[y1:y2, x1:x2]

    @classmethod
    def _calc_hs_hist(cls, roi_hsv: np.ndarray) -> np.ndarray:
        hist = cv2.calcHist([roi_hsv], [0, 1], None, cls._HIST_BINS, cls._HIST_RANGE)
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        return hist

    @staticmethod
    def _group_boxes_by_y(boxes: List[List[int]], y_tol: int) -> List[List[List[int]]]:
        grouped_rows: List[Tuple[float, List[List[int]]]] = []
        for box in sorted(boxes, key=lambda b: b[1]):
            cy = box[1] + box[3] / 2
            placed = False
            for idx, (row_cy, row_boxes) in enumerate(grouped_rows):
                if abs(cy - row_cy) <= y_tol:
                    row_boxes.append(box)
                    new_cy = (row_cy * (len(row_boxes) - 1) + cy) / len(row_boxes)
                    grouped_rows[idx] = (new_cy, row_boxes)
                    placed = True
                    break
            if not placed:
                grouped_rows.append((cy, [box]))
        return [row_boxes for _, row_boxes in grouped_rows]

    @staticmethod
    def _row_bg_foreground_mask(row_img: np.ndarray) -> np.ndarray:
        counts = np.bincount(row_img.flatten())
        bg_val = np.argmax(counts)
        return np.abs(row_img.astype(np.int16) - bg_val) > 25

    @staticmethod
    def _clamp_topk_window(chunk: List[List[int]], max_count: int) -> List[List[int]]:
        if len(chunk) <= max_count:
            return chunk
        start = (len(chunk) - max_count) // 2
        return chunk[start:start + max_count]

    @staticmethod
    def _icon_crop_with_pad(img: Image.Image, box: List[int], pad: int = 2) -> Image.Image:
        x, y, w, h = box
        if w > 2 * pad and h > 2 * pad:
            return img.crop((x + pad, y + pad, x + w - pad, y + h - pad))
        return img.crop((x, y, x + w, y + h))

    @staticmethod
    def _legacy_cutting(img: Image.Image, mode: int):
        """
        old_main.py 的 cutting 逻辑迁移版。
        mode=1: 返回最大矩形区域裁剪结果与边框
        mode=2: 返回头像框候选与被排除的其他框
        """
        im_grey = img.convert('L')
        tot_area = im_grey.size[0] * im_grey.size[1]
        im_grey = im_grey.point(lambda x: 255 if x > 210 else 0)
        thresh = np.array(im_grey)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        areas = []
        icon = []
        for contour in contours:
            area = cv2.contourArea(contour)
            areas.append(area)
            if area > 500 and mode == 2:
                x, y, w, h = cv2.boundingRect(contour)
                if h > 0 and 0.95 < (w / h) < 1.05:
                    side = (w + h) // 2
                    area_ratio = side * side / tot_area * 100 if tot_area > 0 else 0
                    if area_ratio >= 0.5:
                        icon.append([side, [x, y, w, h]])

        if mode == 1:
            if not areas:
                raise ValueError("no contour found in legacy cutting")
            idx = areas.index(max(areas))
            x, y, w, h = cv2.boundingRect(contours[idx])
            cropped = thresh[y + 2:y + h - 2, x + 2:x + w - 2]
            return Image.fromarray(cropped), [x, y, w, h]

        if mode == 2:
            if not icon:
                return [], []

            kinds = {}
            for side, box in icon:
                category = -1
                for kind in kinds:
                    ratio = side / kind
                    if 0.9 < ratio < 1.1:
                        category = kind
                        kinds[kind].append(box)
                        break
                if category == -1:
                    kinds[side] = [box]

            def cluster_weight(item):
                side = item[0]
                count = len(item[1])
                if count == 5:
                    return 5000000 + side
                if count % 5 == 0:
                    return 1000000 + side
                return count * 10000 + side

            kinds_sorted = sorted(kinds.items(), key=cluster_weight, reverse=True)
            kind = kinds_sorted[0]
            if len(kind[1]) % 5 == 0:
                otherborder = []
                for other_kind in kinds_sorted[1:]:
                    otherborder.extend(other_kind[1])
                return kind[1], otherborder
            return [item[1] for item in icon], []

        raise ValueError(f"unsupported legacy cutting mode: {mode}")

    @staticmethod
    def _legacy_cut(img: Image.Image, border: List[int]) -> Image.Image:
        x, y, w, h = border
        img_arr = np.array(img)
        img_arr = img_arr[y + 2:y + h - 2, x + 2:x + w - 2]
        return Image.fromarray(img_arr)

    @staticmethod
    def _legacy_split_last_col_recs(recs: List[Tuple[int, int, int, int]]) -> Tuple[List[Tuple[int, int, int, int]], List[Tuple[int, int, int, int]]]:
        if not recs:
            return [], []
        recs_sorted = sorted(recs, key=lambda x: x[0], reverse=True)
        last_col_recs = [rec for rec in recs_sorted if abs(rec[0] - recs_sorted[0][0]) < recs_sorted[0][2] / 2]
        last_col_recs = sorted(last_col_recs, key=lambda x: x[1])
        remaining = list(set(recs_sorted) - set(last_col_recs))
        return remaining, last_col_recs

    @staticmethod
    def _save_lru_result(cache: OrderedDict[bytes, Tuple[int, int]], key: bytes, value: Tuple[int, int], max_size: int):
        cache[key] = value
        cache.move_to_end(key)
        if len(cache) > max_size:
            cache.popitem(last=False)

    @staticmethod
    def _resolve_match_result(best_uid: int, similarity: int, db, threshold: int = 60) -> Tuple[int, int, str, int]:
        unit_id = best_uid // 100
        star = int((best_uid % 100) / 10)
        if similarity < threshold or (unit_id * 100 + 1) not in db.unit_data:
            return 0, 0, "Unknown", similarity
        return unit_id, star, db.get_unit_name(unit_id * 100 + 1), similarity

    @classmethod
    def _prepare_query_features(cls, img: Image.Image) -> Tuple[bytes, np.ndarray, np.ndarray, np.ndarray]:
        rgb_img = img.convert("RGB").resize((128, 128))
        img_np = np.array(rgb_img)
        cache_digest = hashlib.md5(img_np.tobytes()).digest()
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        img_hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
        hist = cls._calc_hs_hist(cls._extract_roi(img_hsv))
        return cache_digest, img_np, img_gray, hist

    def _load_lru_result(self, cache_key: bytes) -> Optional[Tuple[int, int]]:
        cached = self._unit_result_cache.get(cache_key)
        if cached is None:
            return None
        self._unit_result_cache.move_to_end(cache_key)
        return cached

    def _collect_old_candidates(self, img_np: np.ndarray, hist: np.ndarray) -> List[int]:
        candidate_uids = set()

        img_roi_arr = self._extract_roi(img_np)
        current_hash = self._compute_hash(Image.fromarray(img_roi_arr))
        if self._hash_arr.size > 0:
            dists = np.abs(self._hash_arr - current_hash).sum(axis=1)
            top_idx = self._topk_indices(dists, 10, largest=False)
            candidate_uids.update(self._uid_arr[top_idx].tolist())

        if self._hist_centered_arr.size > 0:
            hist_flat = hist.reshape(-1).astype(np.float32)
            hist_centered = hist_flat - np.mean(hist_flat)
            q_norm = float(np.linalg.norm(hist_centered))
            if q_norm > 1e-8:
                corr_num = self._hist_centered_arr @ hist_centered
                corr_den = self._hist_norm_arr * q_norm
                corr = np.divide(
                    corr_num,
                    corr_den,
                    out=np.full_like(corr_num, -1.0, dtype=np.float32),
                    where=corr_den > 1e-8
                )
                top_idx = self._topk_indices(corr, 10, largest=True)
                candidate_uids.update(self._uid_arr[top_idx].tolist())

        if not candidate_uids:
            return [int(uid) for uid in self._uid_arr.tolist()]
        return sorted(int(uid) for uid in candidate_uids)

    def _collect_cv_candidates(self, hist: np.ndarray, top_n: int) -> List[int]:
        if self._uid_arr.size <= 0:
            return []

        candidates = []
        for uid in self._uid_arr.tolist():
            uid_int = int(uid)
            hist_score = cv2.compareHist(self._templates[uid_int].hist, hist, cv2.HISTCMP_CORREL)
            candidates.append((uid_int, float(hist_score)))
        candidates.sort(key=lambda item: item[1], reverse=True)
        return [uid for uid, _ in candidates[:top_n]]

    def _run_template_match(
        self,
        img_gray: np.ndarray,
        candidate_uids: List[int],
        use_scaled_templates: bool,
        early_stop: float = 2.0,
    ) -> Tuple[int, float]:
        best_score = -1.0
        best_uid = 0

        for uid in candidate_uids:
            if uid not in self._templates:
                continue

            if use_scaled_templates:
                template_list = self._template_scaled_cache.get(uid, [self._templates[uid].template])
            else:
                template_list = [self._templates[uid].template]

            for template in template_list:
                if template.shape[0] > img_gray.shape[0] or template.shape[1] > img_gray.shape[1]:
                    continue

                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > best_score:
                    best_score = max_val
                    best_uid = uid

                if best_score >= early_stop:
                    break

        return best_uid, best_score

    async def _process_image_data(self, full_img: Image.Image) -> UnitCell:
        roi = self._extract_roi(np.array(full_img))
        
        if roi.ndim == 3:
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
            roi_hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        else:
            roi_gray = roi
            roi_hsv = roi 
            
        hist = self._calc_hs_hist(roi_hsv)
        
        return UnitCell(
            hist=hist,
            template=roi_gray,
            arr_hash=self._compute_hash(Image.fromarray(roi)),
            md5=hashlib.md5(np.array(full_img).tobytes()).hexdigest()
        )

    def _rebuild_feature_cache(self):
        if not self._templates:
            self._uid_arr = np.empty((0,), dtype=np.int32)
            self._hash_arr = np.empty((0, 0), dtype=np.uint8)
            self._hist_centered_arr = np.empty((0, 0), dtype=np.float32)
            self._hist_norm_arr = np.empty((0,), dtype=np.float32)
            self._template_scaled_cache = {}
            self._unit_result_cache.clear()
            return

        # 使用稳定顺序构建矩阵，避免 dict 迭代顺序差异影响候选一致性
        uids = np.array(sorted(self._templates.keys()), dtype=np.int32)

        hashes = []
        hists = []
        for uid in uids:
            info = self._templates[int(uid)]
            hashes.append(np.asarray(info.arr_hash, dtype=np.uint8).reshape(-1))
            hists.append(np.asarray(info.hist, dtype=np.float32).reshape(-1))

        hash_arr = np.vstack(hashes)
        hist_arr = np.vstack(hists)
        hist_mean = np.mean(hist_arr, axis=1, keepdims=True)
        hist_centered = hist_arr - hist_mean
        hist_norm = np.linalg.norm(hist_centered, axis=1).astype(np.float32)

        self._uid_arr = uids
        self._hash_arr = hash_arr
        self._hist_centered_arr = hist_centered
        self._hist_norm_arr = hist_norm

        self._template_scaled_cache = {}
        for uid in uids.tolist():
            template = self._templates[uid].template
            h_t, w_t = template.shape[:2]
            scaled_templates = []
            for s in self._TEMPLATE_SCALES:
                new_w = int(w_t * s)
                if new_w <= 0:
                    continue
                scaled_templates.append(cv2.resize(template, (new_w, h_t)))
            self._template_scaled_cache[uid] = scaled_templates

        # 模板更新后清空结果缓存，避免旧结果污染
        self._unit_result_cache.clear()

    async def update_dic(self):
        from ..db.database import db
        async with self._lock:
            if self.init and self.ver == imagemgr.ver:
                return

            self._templates = {}
            if self.data_path.exists():
                try:
                    with open(self.data_path, 'rb') as f:
                        self._templates = pickle.load(f)
                except Exception:
                    self._templates = {}

            updated = False
            for uid in db.unlock_unit_condition:
                uid = uid // 100
                for star in [1, 3, 6]:
                    uid_id = uid * 100 + star * 10 + 1
                    if uid_id in self._templates:
                        continue

                    img = await imagemgr.unit_icon(uid, star)
                    if img:
                        md5_new = hashlib.md5(np.array(img).tobytes()).hexdigest()
                        if uid_id not in self._templates or self._templates[uid_id].md5 != md5_new:
                            self._templates[uid_id] = await self._process_image_data(img)
                            updated = True

            if updated:
                with open(self.data_path, 'wb') as f:
                    pickle.dump(self._templates, f)

            self._rebuild_feature_cache()
            
            self.init = True
            self.ver = imagemgr.ver

    async def _ensure_loaded(self):
        if not self.init or self.ver != imagemgr.ver:
            await self.update_dic()

    async def recognize_unit_old(self, img: Image.Image) -> Tuple[int, int, str, int]:
        await self._ensure_loaded()
        if not self._templates:
            return 0, 0, "Unknown", 0

        from ..db.database import db

        cache_digest, img_np, img_gray, hist = self._prepare_query_features(img)
        cache_key = b"old:" + cache_digest
        cached = self._load_lru_result(cache_key)
        if cached is not None:
            best_uid, similarity = cached
            return self._resolve_match_result(best_uid, similarity, db, threshold=60)

        top_uids = self._collect_old_candidates(img_np, hist)
        best_uid, best_score = self._run_template_match(
            img_gray,
            top_uids,
            use_scaled_templates=True,
            early_stop=0.95,
        )
        similarity = int(best_score * 100)
        self._save_lru_result(
            self._unit_result_cache,
            cache_key,
            (best_uid, similarity),
            self._unit_result_cache_max
        )
        return self._resolve_match_result(best_uid, similarity, db, threshold=60)

    async def recognize_unit(self, img: Image.Image) -> Tuple[int, int, str, int]:
        """
        cv.py 迁移版识别逻辑：
        1) HS直方图筛选 Top-N 候选
        2) 候选模板做 CCOEFF_NORMED 匹配
        """
        await self._ensure_loaded()
        if not self._templates:
            return 0, 0, "Unknown", 0

        from ..db.database import db

        cache_digest, _, img_gray, hist = self._prepare_query_features(img)
        cache_key = b"cv:" + cache_digest
        cached = self._load_lru_result(cache_key)
        if cached is not None:
            best_uid, similarity = cached
            return self._resolve_match_result(best_uid, similarity, db, threshold=50)

        top_uids = self._collect_cv_candidates(hist, self._CV_HIST_TOP_N)
        if not top_uids:
            top_uids = [int(uid) for uid in self._uid_arr.tolist()]

        best_uid, best_score = self._run_template_match(
            img_gray,
            top_uids,
            use_scaled_templates=False,
        )
        similarity = int(best_score * 100)
        self._save_lru_result(
            self._unit_result_cache,
            cache_key,
            (best_uid, similarity),
            self._unit_result_cache_max
        )
        return self._resolve_match_result(best_uid, similarity, db, threshold=50)

    @staticmethod
    def _find_segments(projection: np.ndarray, threshold: float, min_gap: int = 0, min_len: int = 0) -> List[Tuple[int, int]]:
        """在投影中寻找连续的段"""
        segments = []
        start = -1
        gap = 0
        
        for i, val in enumerate(projection):
            if val > threshold:
                if start == -1: start = i
                gap = 0
            else:
                if start != -1:
                    gap += 1
                    if gap > min_gap:
                        if (i - gap) - start >= min_len:
                            segments.append((start, i - gap))
                        start = -1
                        gap = 0
        
        if start != -1 and len(projection) - start >= min_len:
            segments.append((start, len(projection)))
            
        return segments

    @staticmethod
    def detect_cells(img: Image.Image) -> Tuple[List[Tuple[int, int, int, int]], List[Tuple[int, int, int, int]]]:
        """
        检测图像中的单元格位置（基于网格特征）
        Returns: (valid_boxes, excluded_boxes)
        """
        img_gray = img.convert('L')
        img_arr = np.array(img_gray)
        img_h = img_arr.shape[0]
        
        # Canny边缘检测
        edges = cv2.Canny(img_arr, 50, 150)
        
        # 水平投影找行
        kernel_row = np.ones((1, 1), np.uint8) 
        edges_row = cv2.dilate(edges, kernel_row, iterations=1)
        row_proj = np.sum(edges_row, axis=1)
        
        def estimate_base_size(row_heights: List[int]) -> float:
            if not row_heights:
                return 0.0
            arr = np.array(row_heights, dtype=np.float32)
            best_group = arr
            best_score = -1.0
            # 用“数量 * 高度”找主簇，避免被大量短文本行拉低。
            for h_val in arr:
                tol = max(3.0, float(h_val) * 0.22)
                group = arr[np.abs(arr - h_val) <= tol]
                score = len(group) * float(np.median(group))
                if score > best_score:
                    best_score = score
                    best_group = group
            return float(np.median(best_group))

        def build_row_candidates(row_thresh_ratio: float) -> Tuple[List[Tuple[int, int]], float, List[Tuple[int, int]]]:
            if np.max(row_proj) <= 0:
                return [], 0.0, []
            row_thresh = np.max(row_proj) * row_thresh_ratio
            segments = UnitRecognizer._find_segments(row_proj, row_thresh, min_gap=0, min_len=16)
            if not segments:
                return [], 0.0, []
            base_size = estimate_base_size([end - start for start, end in segments])
            normal_rows = []
            if base_size > 0:
                for y1, y2 in segments:
                    h_row = y2 - y1
                    if 0.65 <= (h_row / base_size) <= 1.35:
                        normal_rows.append((y1, y2))
            return segments, base_size, normal_rows

        row_segments, base_size, normal_rows = build_row_candidates(0.1)

        # 宽图长表格经常在底部出现弱边缘行，必要时降低阈值补齐。
        has_short_bottom_row = (
            base_size > 0
            and any((y2 - y1) < base_size * 0.5 and y1 > img_h * 0.72 for y1, y2 in row_segments)
        )
        if has_short_bottom_row and len(normal_rows) <= 6:
            row_segments_lo, base_size_lo, normal_rows_lo = build_row_candidates(0.07)
            if len(normal_rows_lo) > len(normal_rows):
                row_segments = row_segments_lo
                base_size = base_size_lo
                normal_rows = normal_rows_lo

        if not normal_rows or base_size <= 0:
            return [], []
        
        valid_boxes = []
        excluded_boxes = []
        normal_set = set(normal_rows)

        for y1, y2 in row_segments:
            h_row = y2 - y1
            if (y1, y2) not in normal_set:
                excluded_boxes.append((0, y1, 0, h_row))
                continue
            
            row_img = img_arr[y1:y2, :]
            fg_mask = UnitRecognizer._row_bg_foreground_mask(row_img)
            col_proj = np.sum(fg_mask, axis=0)
            col_thresh = h_row * 0.15 
            
            # 垂直投影找列
            col_segments = UnitRecognizer._find_segments(col_proj, col_thresh, min_gap=5, min_len=int(base_size * 0.8))
            
            for sx, ex in col_segments:
                w_seg = ex - sx
                unit_count = int(round(w_seg / base_size))
                if unit_count < 1: unit_count = 1
                
                unit_w = w_seg / unit_count
                
                for k in range(unit_count):
                    bx = sx + k * unit_w
                    bw = unit_w
                    if bw < 8: continue
                    valid_boxes.append([int(bx), y1, int(bw), int(h_row)])

        if not valid_boxes:
            return [], excluded_boxes

        # 后处理：按行切块，并对明显过长的块限制为最多5个头像。
        row_tol = max(10, int(base_size * 0.45))
        grouped_rows = UnitRecognizer._group_boxes_by_y(valid_boxes, row_tol)

        refined_boxes: List[List[int]] = []
        for row_boxes in grouped_rows:
            row_boxes = sorted(row_boxes, key=lambda b: b[0])
            if not row_boxes:
                continue

            centers = [b[0] + b[2] / 2 for b in row_boxes]
            gaps = [centers[i + 1] - centers[i] for i in range(len(centers) - 1)]
            median_gap = float(np.median(gaps)) if gaps else base_size
            split_gap = max(base_size * 1.5, median_gap * 1.8)

            chunks: List[List[List[int]]] = []
            chunk = [row_boxes[0]]
            for i, gap in enumerate(gaps):
                if gap > split_gap:
                    chunks.append(chunk)
                    chunk = [row_boxes[i + 1]]
                else:
                    chunk.append(row_boxes[i + 1])
            chunks.append(chunk)

            max_chunk_len = max(len(c) for c in chunks)
            for chunk in chunks:
                # 右侧作者头像/杂点常表现为很短的独立块。
                if max_chunk_len >= 5 and len(chunk) < 3:
                    continue
                raw_len = len(chunk)
                chunk = UnitRecognizer._clamp_topk_window(chunk, 5)
                if raw_len > 5:
                    # 超长块通常包含编号/伤害文本，收紧框体到头像主体。
                    if raw_len >= 7 and base_size >= 110:
                        shrinked_chunk = []
                        for bx, by, bw, bh in chunk:
                            side = max(8, int(round(min(bw, bh) * 0.78)))
                            nx = bx + max(0, (bw - side) // 2)
                            ny = by + max(0, int(round((bh - side) * 0.03)))
                            shrinked_chunk.append([nx, ny, side, side])
                        chunk = shrinked_chunk
                refined_boxes.extend(chunk)
        
        return refined_boxes, excluded_boxes

    @staticmethod
    def detect_content_area(img: Image.Image) -> Tuple[Optional[Image.Image], Optional[Tuple[int, int, int, int]]]:
        """
        检测主要内容区域并进行裁剪
        """
        img_gray = img.convert('L')
        img_arr = np.array(img_gray)
        
        edges = cv2.Canny(img_arr, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None
            
        max_area = 0
        max_rect = None
        
        # 寻找最大边缘轮廓作为内容主体
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            if area > max_area and w > 16 and h > 16:
                max_area = area
                max_rect = (x, y, w, h)
        
        if max_rect:
            x, y, w, h = max_rect
            cropped = img.crop((x, y, x+w, y+h))
            return cropped, (x, y, w, h)
            
        return None, None

    async def _detect_rows_legacy(self, image: Image.Image) -> List[List[List[int]]]:
        """
        先使用 old_main.py 的 cutting/getPos 思路定位头像框。
        这里只复用旧版找框逻辑，单头像识别仍走当前 recognize_unit。
        """
        current_img = image.convert("RGBA")
        current_detect_img = current_img
        actual_offset_x = 0
        actual_offset_y = 0

        for attempt in range(6):
            border, _ = self._legacy_cutting(current_detect_img, 2)
            no_box_found = len(border) == 0

            if border and len(border) >= 4:
                recs = set(tuple(rec) for rec in border)
                _, last_col_recs = self._legacy_split_last_col_recs(list(recs))
                row_cnt = len(last_col_recs)

                if row_cnt > 0:
                    arr: List[List[Optional[Tuple[int, int, int, int]]]] = [[None for _ in range(5)] for _ in range(row_cnt)]
                    last_col_recs_ypos = [rec[1] for rec in last_col_recs]
                    working_recs = list(recs)

                    for col_index in range(5):
                        working_recs, last_col_recs = self._legacy_split_last_col_recs(working_recs)
                        if not last_col_recs:
                            break

                        for rec in last_col_recs:
                            cell_crop = self._icon_crop_with_pad(current_img, list(rec), pad=2)
                            uid, _, _, _ = await self.recognize_unit(cell_crop)
                            if uid == 0:
                                continue

                            most_near_row = 0
                            for row_index in range(1, len(arr)):
                                if abs(last_col_recs_ypos[row_index] - rec[1]) < abs(last_col_recs_ypos[most_near_row] - rec[1]):
                                    most_near_row = row_index

                            existing = arr[most_near_row][col_index]
                            if existing is None or abs(last_col_recs_ypos[most_near_row] - existing[1]) > abs(last_col_recs_ypos[most_near_row] - rec[1]):
                                arr[most_near_row][col_index] = rec

                    rows = []
                    for row in arr:
                        none_cnt = row.count(None)
                        if none_cnt >= 2:
                            continue

                        ordered_row = [row[4 - col_index] for col_index in range(5) if row[4 - col_index] is not None]
                        if not ordered_row:
                            continue

                        rows.append([
                            [x + actual_offset_x, y + actual_offset_y, w, h]
                            for x, y, w, h in ordered_row
                        ])

                    if rows:
                        return rows

            try:
                next_detect_img, border_rect = self._legacy_cutting(current_detect_img, 1)
            except Exception:
                return []

            if attempt == 0 or no_box_found:
                next_detect_img = next_detect_img.point(lambda x: 0 if x > 128 else 255)

            current_img = self._legacy_cut(current_img, border_rect)
            current_detect_img = next_detect_img
            actual_offset_x += border_rect[0]
            actual_offset_y += border_rect[1]

        return []

    def _detect_rows_modern(self, image: Image.Image) -> List[List[List[int]]]:
        """
        新版基于投影/Canny 的找框逻辑。
        """
        current_img = image.convert("RGBA")
        actual_offset_x = 0
        actual_offset_y = 0

        for _ in range(6):
            valid_boxes, _ = self.detect_cells(current_img)
            if valid_boxes:
                global_boxes = [[x + actual_offset_x, y + actual_offset_y, w, h] for x, y, w, h in valid_boxes]
                return self._group_boxes_by_y(global_boxes, 15)

            cropped, rect = self.detect_content_area(current_img)
            if cropped is None or rect is None:
                return []

            current_img = cropped
            cx, cy, _, _ = rect
            actual_offset_x += cx
            actual_offset_y += cy

        return []

    async def _render_recognition(self, img: Image.Image, rows: List[List[List[int]]], debug: bool = False, d_file: str = "") -> Tuple[List[List[int]], str]:
        arr_uids_final = []

        outp_img = img.copy()
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 160))
        outp_img = Image.alpha_composite(outp_img, overlay)
        draw_outp = ImageDraw.Draw(outp_img)

        row_cnt = len(rows)
        max_cols = max((len(r) for r in rows), default=0)
        icon_size = 64

        compare_w = max(1, icon_size * max_cols + 16 * 2)
        compare_h = max(1, icon_size * 2 * row_cnt + 16 * (row_cnt + 1))
        compare_img = Image.new("RGBA", (compare_w, compare_h), (255, 255, 255, 255))

        for r_idx, r_list in enumerate(rows):
            r_list = sorted(r_list, key=lambda b: b[0])
            row_uids = []

            for c_idx, rec in enumerate(r_list):
                rx, ry, rw, rh = rec
                cell_crop = self._icon_crop_with_pad(img, rec, pad=2)

                uid, star, name, score = await self.recognize_unit(cell_crop)

                if debug:
                    print(f"Recognized: {name} (ID: {uid}), score: {score}")

                paste_x = rx + 2 if rw > 4 else rx
                paste_y = ry + 2 if rh > 4 else ry
                outp_img.paste(cell_crop, (paste_x, paste_y))

                color = "red" if uid != 0 else "black"
                draw_outp.rectangle((rx, ry, rx + rw, ry + rh), outline=color, width=3)

                pos_x = 16 + icon_size * c_idx
                pos_y = 16 * (r_idx + 1) + icon_size * 2 * r_idx

                cell_resize = cell_crop.resize((64, 64))
                compare_img.paste(cell_resize, (pos_x, pos_y))

                if uid != 0:
                    try:
                        icon_bytes = await imagemgr.unit_icon(uid, star)
                        if icon_bytes:
                            icon = icon_bytes.convert("RGBA").resize((64, 64))
                            compare_img.paste(icon, (pos_x, pos_y + 64), icon)
                            row_uids.append(uid)
                    except Exception as e:
                        if debug:
                            print(f"Icon load failed: {e}")

            row_uids.reverse()
            arr_uids_final.append(row_uids)

        def img_to_b64(im):
            buf = BytesIO()
            im.save(buf, format='PNG')
            return f'[CQ:image,file=base64://{base64.b64encode(buf.getvalue()).decode()}]'

        if debug and d_file:
            try:
                p = Path(d_file)
                outp_img.save(p.parent / f"{p.stem}_outp.png")
                compare_img.save(p.parent / f"{p.stem}_compare.png")
            except Exception:
                pass

        return arr_uids_final, f'{img_to_b64(outp_img)}\n{img_to_b64(compare_img)}'

    async def recognize(self, image: Image.Image, debug: bool = False, d_file: str = "") -> Tuple[List[List[int]], str]:
        """
        主入口：检测并识别图片中的所有角色
        """
        img = image.convert("RGBA")
        rows = await self._detect_rows_legacy(img)
        if not rows:
            rows = self._detect_rows_modern(img)
        if not rows:
            return [], ""
        return await self._render_recognition(img, rows, debug=debug, d_file=d_file)


# Global instance
instance = UnitRecognizer.get_instance()

async def main():
    files = sorted(Path(".").glob("test*.png"), key=lambda p: p.name)
    
    recognizer = UnitRecognizer.get_instance()
    for file in files:
        print(f"Processing {file.name}...")
        try:
            img = Image.open(file)
            res, _ = await recognizer.recognize(img, debug=True, d_file=str(file))
            print("Result IDs:", res)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
