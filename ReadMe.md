名称：直播翻译

1、音频转录模型：Systran/faster-whisper-base.en ,默认只转录英语,如果想转录其他语言则在TranscriberModels中修改WhisperModel的模型,模型下载途径:https://huggingface.co/Systran

2、翻译则选择Google翻译,因为速度够快，符合实时需求，但是实际情况取决于用户的网络的质量

3、可在AudioTranscriber修改PHRASE_TIMEOUT参数，其代表着静默时长，用于划分句子

4、AudioRecorder中参数RECORD_TIMEOUT代表每次录制音频时长
