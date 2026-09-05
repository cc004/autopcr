# ============ module/notify.py ============

import smtplib
from email.header import Header
from email.mime.text import MIMEText

from ...model.enums import *
from ...model.error import *
from ...util.logger import instance as logger
from ..config import *
from ..modulebase import *

# ============ 配置定义 ============

EMAIL_PROVIDERS = ["QQ邮箱", "163邮箱", "126邮箱"]

SMTP_CONFIGS = {
    "QQ邮箱": {"host": "smtp.qq.com", "port": 587},
    "163邮箱": {"host": "smtp.163.com", "port": 465},
    "126邮箱": {"host": "smtp.126.com", "port": 465},
}


# ============ 抽象基类 ============

class NotifyModule(Module):
    """通知模块抽象基类"""

    def is_configured(self) -> bool:
        raise NotImplementedError

    async def send_notification(
        self, subject: str, body: str, is_html: bool = False
    ) -> bool:
        raise NotImplementedError


# ============ SMTP 实现 ============

class SmtpNotify(NotifyModule):
    """SMTP 邮件通知实现（每次新建实例，但复用连接）"""

    # 🔥 类变量共享 SMTP 连接（所有实例复用同一个连接）
    _server = None

    def __init__(self, modulemgr=None):
        super().__init__(modulemgr)

    def get_notify_email_enable(self) -> bool:
        return self.get_config("notify_email_enable")

    def get_notify_email_user(self) -> str:
        return self.get_config("notify_email_user")

    def get_notify_email_to(self) -> str:
        return self.get_config("notify_email_to")

    def get_notify_email_password(self) -> str:
        return self.get_config("notify_email_password")

    def get_notify_email_provider(self) -> str:
        return self.get_config("notify_email_provider")

    def get_smtp_config(self) -> dict:
        provider = self.get_notify_email_provider()
        return SMTP_CONFIGS.get(provider, SMTP_CONFIGS["QQ邮箱"])

    def _get_server(self):
        """获取或创建 SMTP 连接（类级别复用）"""
        if SmtpNotify._server is not None:
            return SmtpNotify._server

        smtp = self.get_smtp_config()
        try:
            if smtp.get("port") == 465:
                server = smtplib.SMTP_SSL(smtp["host"], smtp["port"])
            else:
                server = smtplib.SMTP(smtp["host"], smtp["port"])
                server.starttls()

            user = self.get_notify_email_user()
            password = self.get_notify_email_password()
            server.login(user, password)

            SmtpNotify._server = server
            return server

        except smtplib.SMTPException as e:
            logger.error(f"SMTP 连接失败: {e}")
            return None
        except Exception as e:
            logger.exception("连接失败: ")
            return None

    def _close_server(self):
        """关闭 SMTP 连接"""
        if SmtpNotify._server is not None:
            try:
                SmtpNotify._server.quit()
            except Exception as e:
                logger.exception("关闭 SMTP 连接时出错:")
            SmtpNotify._server = None

    def is_configured(self) -> bool:
        enable = self.get_notify_email_enable()
        user = self.get_notify_email_user()
        to = self.get_notify_email_to()
        password = self.get_notify_email_password()
        
        if not enable:
            return False
        if not bool(user):
            return False
        if not bool(to):
            return False
        return bool(password)

    async def send_notification(
        self, subject: str, body: str, is_html: bool = False
    ) -> bool:
        if not self.is_configured():
            logger.warning("邮件通知未配置，跳过发送")
            return False

        user = self.get_notify_email_user()
        to = self.get_notify_email_to()

        content_type = "html" if is_html else "plain"
        msg = MIMEText(body, content_type, "utf-8")
        msg["From"] = Header(user)
        msg["To"] = Header(to)
        msg["Subject"] = Header(subject, "utf-8")

        try:
            server = self._get_server()
            if server is None:
                return False

            server.sendmail(user, [to], msg.as_string())
            logger.info(f"邮件发送成功: {subject} -> {to}")
            return True

        except smtplib.SMTPServerDisconnected:
            logger.warning("SMTP 连接已断开，尝试重新连接...")
            self._close_server()
            server = self._get_server()
            if server is None:
                logger.error("重新连接 SMTP 失败")
                return False
            try:
                server.sendmail(user, [to], msg.as_string())
                logger.info(f"邮件重发成功: {subject} -> {to}")
                return True
            except Exception as e:
                logger.exception("重发邮件失败: ")
                return False

        except smtplib.SMTPException as e:
            logger.exception("SMTP 邮件发送失败: ")
            self._close_server()
            return False
        except Exception:
            logger.exception("邮件发送失败:")
            return False


# ============ 配置类 ============

@texttype("notify_email_to", "接收通知的邮箱", "")
@texttype("notify_email_password", "邮箱授权码", "")
@texttype("notify_email_user", "发送通知的邮箱", "")
@singlechoice("notify_email_provider", "邮箱服务商", "QQ邮箱", EMAIL_PROVIDERS)
@booltype("notify_email_enable", "启用邮件通知", False)
@description("邮件通知配置 - 任务完成后发送邮件提醒")
@name("邮件通知")
@default(False)
@notrunnable
class email_notify(SmtpNotify):
    """邮件通知模块"""