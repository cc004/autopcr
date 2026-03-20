#!/usr/bin/env python3
"""
邮件通知脚本 - 使用 yagmail 发送 HTML 内嵌图片邮件
环境变量配置:
    MAIL_FROM: 发件人邮箱地址
    MAIL_PASSWORD: 邮箱授权码（不是登录密码）
    MAIL_TO: 收件人邮箱地址（多个用逗号分隔）
"""

import os
import io
import base64
from typing import List, Optional
from .logger import instance as logger
import yagmail

# 直接导入 PIL
from PIL import Image


class MailNotifier:
    """邮件通知类 - 支持 QQ 和 163 邮箱"""
    
    # 邮箱服务商配置映射表
    MAIL_CONFIGS = {
        'qq.com': {
            'host': 'smtp.qq.com',
            'port': 465,
            'ssl': True,
            'description': 'QQ邮箱'
        },
        '163.com': {
            'host': 'smtp.163.com',
            'port': 465,
            'ssl': True,
            'description': '163邮箱'
        }
    }
    
    def __init__(self):
        """初始化邮件配置"""
        # 必需的环境变量
        self.mail_from = os.getenv('MAIL_FROM')
        self.mail_password = os.getenv('MAIL_PASSWORD')
        self.mail_to = os.getenv('MAIL_TO')
        
        # 验证必要配置
        self._validate_config()
        
        # 获取邮箱服务商配置
        self.mail_config = self._get_mail_config()
        
        # 初始化 yagmail
        self._init_yagmail()
    
    def _validate_config(self):
        """验证必要的配置是否存在"""
        missing = []
        if not self.mail_from:
            missing.append('MAIL_FROM')
        if not self.mail_password:
            missing.append('MAIL_PASSWORD')
        if not self.mail_to:
            missing.append('MAIL_TO')
        
        if missing:
            raise ValueError(f"缺少必要的环境变量: {', '.join(missing)}")
    
    def _get_mail_config(self):
        """根据邮箱地址获取对应的服务商配置"""
        domain = self.mail_from.split('@')[-1].lower()
        
        for key, config in self.MAIL_CONFIGS.items():
            if domain == key or domain.endswith('.' + key):
                logger.info(f"检测到邮箱类型: {config['description']}")
                return config
        
        logger.warning(f"未找到 {domain} 的配置，默认使用 QQ 邮箱配置")
        return self.MAIL_CONFIGS['qq.com']
    
    def _init_yagmail(self):
        """初始化 yagmail 连接"""
        try:
            self.to_list = [email.strip() for email in self.mail_to.split(',')]
            
            self.yag = yagmail.SMTP(
                user=self.mail_from,
                password=self.mail_password,
                host=self.mail_config['host'],
                port=self.mail_config['port'],
                smtp_ssl=self.mail_config['ssl']
            )
            
            logger.info(f"邮件服务初始化成功: {self.mail_from} -> {self.mail_config['description']}")
            
        except Exception as e:
            logger.error(f"邮件服务初始化失败: {e}")
            raise
    
    def _img_to_base64(self, img: Image.Image, format: str = 'PNG') -> str:
        """
        将 PIL Image 对象转换为 base64 字符串
        
        Args:
            img: PIL Image.Image 对象
            format: 图片格式，默认 PNG
            
        Returns:
            str: base64 编码的图片数据
        """
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=format)
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
        return img_base64
    
    def send_html_with_image(self,
                            img: Image.Image,
                            title: str = "PCR日常完成通知",
                            extra_text: Optional[str] = None,
                            cc: Optional[List[str]] = None,
                            bcc: Optional[List[str]] = None) -> bool:
        """
        发送包含内嵌图片的 HTML 邮件（使用内联样式）
        
        Args:
            img: PIL Image 对象（从 draw 函数返回的图片）
            title: 邮件标题
            extra_text: 额外说明文字
            cc: 抄送列表
            bcc: 密送列表
            
        Returns:
            bool: 发送成功返回 True，失败返回 False
        """
        try:
            # 转换图片为 base64
            img_base64 = self._img_to_base64(img)
            
            # 构建 HTML 内容（使用内联样式）
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:20px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height:1.6; color:#333; background-color:#f5f5f5;">
    <div style="max-width:800px; margin:0 auto; background-color:#f9f9f9; border-radius:8px; padding:20px; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
        
        <div style="text-align:center; margin-bottom:20px; padding-bottom:10px; border-bottom:2px solid #4CAF50;">
            <h2 style="color:#4CAF50; margin:0; font-size:24px;">✅ {title}</h2>
        </div>
        
        <div style="text-align:center;">
            <p style="margin:0 0 20px 0; font-size:16px;">您的日常任务已完成，以下是执行结果：</p>
            
            <div style="margin:20px 0; text-align:center;">
                <img src="data:image/png;base64,{img_base64}" alt="日常结果" style="max-width:100%; height:auto; border-radius:4px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
            </div>
            
            {f'<div style="background-color:#fff; padding:15px; border-radius:4px; margin:20px 0; text-align:left; border-left:4px solid #4CAF50; font-size:14px;">{extra_text}</div>' if extra_text else ''}
        </div>
        
        <div style="margin-top:20px; padding-top:10px; text-align:center; font-size:12px; color:#999; border-top:1px solid #ddd;">
            <p style="margin:5px 0;">此邮件由系统自动发送，请勿回复</p>
            <p style="margin:5px 0;">发送时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
    </div>
</body>
</html>"""
            
            # 发送邮件
            self.yag.send(
                to=self.to_list,
                cc=cc,
                bcc=bcc,
                subject=title,
                contents=html_content
            )
            
            logger.info(f"HTML邮件发送成功: {title} -> {self.to_list}")
            return True
            
        except Exception as e:
            logger.error(f"HTML邮件发送失败: {e}")
            return False
    
    def close(self):
        """关闭邮件连接"""
        if hasattr(self, 'yag'):
            self.yag.close()
            logger.info("邮件连接已关闭")