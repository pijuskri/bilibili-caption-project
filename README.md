# Bilibili Caption Project
### Translating bilili video subtitles from chinese to english realtime

Many videos on bilibili.com have subs, but they are hardcoded into the video.
I thought of grabbing those subtitles, converting them to text and translating the resulting text into english.
The resulting tool has rough edges, but succesfully provides trsnslations in most scenarios.

## Features
* Screen capture based character recognition
* Screen region select
* Translation using *Deepl* api and locally with *Argos*/*MarianMT*
* Basic UI to select region, show translation

## Requirements
* paddle 2.4.1 
* paddleorc >=2
* python >=3.9
* pytorch >2 (for MariantMT)

#### For GPU support (optional, but cpu only untested)
* Cuda 11.7
* CudNN 8.4
* At least 4GB NVIDIA GPU with cuda support

## Get started
Requirement setup
```bash
git pull https://github.com/pijuskri/bilibili-caption-project.git
pip install -r requirements.txt
```

To run
```bash
python capture.py
```

#### Configuration
*variables.py* contains the api setting used for translation. 
argos, deepl and helsinki(MarianMT) are possible options. 

Keep in mind that deepl use requires an API token. 
Set it using env var "deepl_token".

## Future work
* Make a proper UI
* Find best local translation option that can hopefully match deepl
* Capture video/browser tab directly instead of screen

## Note on gpu support
Spent a lot of time installing everything, as usual for CUDA. 
Seems you have to copy cudNN install into the cuda directory. Also put zlib into the cuda bin.
Below are links that were instrumental in fixing everything

* [Paddle docs](https://www.paddlepaddle.org.cn/documentation/docs/en/install/index_en.html)
* [Nvidia docs](https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#install-windows)
* [Paddle on windows](https://www.codeproject.com/Tips/5347636/Getting-PaddleOCR-and-PaddlePaddle-to-work-in-Wind)
* [Zlib issue](https://stackoverflow.com/questions/72356588/could-not-locate-zlibwapi-dll-please-make-sure-it-is-in-your-library-path)
