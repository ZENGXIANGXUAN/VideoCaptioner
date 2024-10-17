
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Set
import datetime
from random import randint
from enum import Enum

from .bk_asr.ASRData import ASRData


class OutputFormatEnum(Enum):
    """ 输出格式 """
    SRT = "srt"
    ASS = "ass"
    VTT = "vtt"
    JSON = "json"
    TXT = "txt"


class TranscribeModelEnum(Enum):
    """ 转录模型 """
    JIANYING = "剪映"
    BIJIAN = "必剪"
    KUAISHOU = "快手"


class TargetLanguageEnum(Enum):
    """ 目标语言 """
    CHINESE_SIMPLIFIED = "简体中文"
    CHINESE_TRADITIONAL = "繁体中文"
    ENGLISH = "英语"
    JAPANESE = "日语"
    KOREAN = "韩语"
    FRENCH = "法语"
    GERMAN = "德语"
    SPANISH = "西班牙语"
    ITALIAN = "意大利语"
    PORTUGUESE = "葡萄牙语"
    RUSSIAN = "俄语"
    TURKISH = "土耳其语"


@dataclass
class VideoInfo:
    """视频信息类"""
    file_name: str
    width: int
    height: int
    fps: float
    duration_seconds: float
    bitrate_kbps: int
    video_codec: str
    audio_codec: str
    audio_sampling_rate: int
    thumbnail_path: str


SUPPORTED_AUDIO_FORMATS = "Audio files (*.mp3 *.wav *.m4a *.ogg *.opus *.flac);;\
Video files (*.mp4 *.webm *.ogm *.mov *.mkv *.avi *.wmv);;All files (*.*)"

@dataclass
class Task:
    class Status(Enum):
        """ 任务状态 (下载、转录、优化、翻译、生成) """
        PENDING = "待处理"
        DOWNLOADING = "下载中"
        TRANSCRIBING = "转录中"
        OPTIMIZING = "优化中"
        TRANSLATING = "翻译中"
        GENERATING = "合成视频中"
        COMPLETED = "已完成"
        FAILED = "失败"
        CANCELED = "已取消"

    class Source(Enum):
        FILE_IMPORT = "文件导入"
        URL_IMPORT = "URL导入"
    
    # 任务信息
    id: int = field(default_factory=lambda: randint(0, 100_000_000))
    queued_at: Optional[datetime.datetime] = None
    started_at: Optional[datetime.datetime] = None
    completed_at: Optional[datetime.datetime] = None
    status: Status = Status.PENDING
    fraction_downloaded: float = 0.0
    work_dir: Optional[str] = None

    # 初始输入
    file_paths: Optional[str] = None
    url: Optional[str] = None
    source: Source = Source.FILE_IMPORT
    original_language: Optional[str] = None
    target_language: Optional[str] = None
    video_info: Optional[VideoInfo] = None

    # 音频转换
    audio_format: Optional[str] = "mp3"
    audio_save_path: Optional[str] = None

    # 转录（转录模型）
    transcribe_model: Optional[TranscribeModelEnum] = TranscribeModelEnum.JIANYING
    use_asr_cache: bool = True
    original_subtitle_save_path: Optional[str] = None

    # LLM（优化翻译模型）
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    llm_model: Optional[str] = None
    need_translate: bool = True
    need_optimize: bool = True
    result_subtitle_save_path: Optional[str] = None
    thread_num: int = 10
    batch_size: int = 10

    # 视频生成
    video_save_path: Optional[str] = None
    soft_subtitle: bool = True
