"""Simple i18n helpers with optional fluentogram integration."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)


_FALLBACK_MESSAGES: dict[str, dict[str, str]] = {
    "ru": {
        "main_menu_text": (
            "🎯 LeadCore\n\n"
            "Нахожу потенциальных клиентов в Telegram-чатах\n"
            "и присылаю тебе готовые карточки для аутрича."
        ),
        "btn_my_programs": "📋 Мои программы",
        "btn_pains_content": "🔥 Боли и контент",
        "btn_subscription": "💎 Подписка",
        "btn_main_menu": "🏠 Главное меню",
        "btn_back": "◀️ Назад",
        "btn_cancel": "❌ Отмена",
    },
    "en": {
        "main_menu_text": (
            "🎯 LeadCore\n\n"
            "I find potential clients in Telegram chats\n"
            "and send you ready outreach lead cards."
        ),
        "btn_my_programs": "📋 My Programs",
        "btn_pains_content": "🔥 Pains & Content",
        "btn_subscription": "💎 Subscription",
        "btn_main_menu": "🏠 Main Menu",
        "btn_back": "◀️ Back",
        "btn_cancel": "❌ Cancel",
    },
}


def get_locale(language_code: str | None) -> str:
    """Normalize Telegram language code to one of supported locales."""
    if language_code and language_code.lower().startswith("en"):
        return "en"
    return "ru"


def pick(locale: str, ru: str, en: str) -> str:
    """Return locale-specific string from RU/EN variants."""
    return en if locale == "en" else ru


class _FluentogramAdapter:
    """Optional fluentogram wrapper with graceful fallback."""

    def __init__(self) -> None:
        self._hub: Any | None = None
        self._init_failed = False

    def translate(self, locale: str, key: str, **kwargs: Any) -> str | None:
        """Translate key via fluentogram if available; otherwise return None."""
        if self._init_failed:
            return None
        if self._hub is None and not self._try_init():
            return None
        if self._hub is None:
            return None

        try:
            translator = None
            if hasattr(self._hub, "get_translator_by_locale"):
                translator = self._hub.get_translator_by_locale(locale)
            elif hasattr(self._hub, "get_translator"):
                translator = self._hub.get_translator(locale)

            if translator and hasattr(translator, "get"):
                return translator.get(key, **kwargs)
        except Exception as exc:  # pragma: no cover - best effort fallback
            logger.warning("Fluentogram translation failed: %s", exc)
        return None

    def _try_init(self) -> bool:
        """Initialize fluentogram hub lazily."""
        try:
            from fluentogram import TranslatorHub  # type: ignore
            from fluentogram import FluentTranslator  # type: ignore
        except Exception:
            self._init_failed = True
            return False

        base = Path(__file__).resolve().parent.parent / "locales"
        try:
            self._hub = TranslatorHub(
                locales_map={"ru": ("ru",), "en": ("en",)},
                translators=[
                    FluentTranslator(
                        locale="ru",
                        filename=str(base / "ru" / "LC_MESSAGES" / "bot.ftl"),
                    ),
                    FluentTranslator(
                        locale="en",
                        filename=str(base / "en" / "LC_MESSAGES" / "bot.ftl"),
                    ),
                ],
            )
            return True
        except Exception as exc:  # pragma: no cover - best effort fallback
            logger.warning("Failed to initialize fluentogram adapter: %s", exc)
            self._init_failed = True
            return False


_fluentogram = _FluentogramAdapter()


def t(key: str, language_code: str | None = None, **kwargs: Any) -> str:
    """Translate key for user's language code with fallback dictionary."""
    locale = get_locale(language_code)
    translated = _fluentogram.translate(locale, key, **kwargs)
    if translated:
        return translated
    table = _FALLBACK_MESSAGES.get(locale, _FALLBACK_MESSAGES["ru"])
    template = table.get(key) or _FALLBACK_MESSAGES["ru"].get(key) or key
    if kwargs:
        return template.format(**kwargs)
    return template
