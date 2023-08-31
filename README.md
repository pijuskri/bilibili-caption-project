# Bilibili Caption Project
### WIP personal project for translating bilili video subtitles

Many videos on bilibili have subs, but they are hardcoded into the video.
I thought of grabbing those subtitles, converting them to text and translating using an api.

## Requirements
* Cuda 11.7
* CudNN 
* paddle 2.5.1
* paddleorc 


## Note on gpu support
Spent a lot of time installing everything, as usual for CUDA. 
Seems you have to copy cudNN install into the cuda directory. Also put zlib into the cuda bin.
Below are links that were instrumental in fixing everything

https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#install-windows
https://www.codeproject.com/Tips/5347636/Getting-PaddleOCR-and-PaddlePaddle-to-work-in-Wind
https://stackoverflow.com/questions/72356588/could-not-locate-zlibwapi-dll-please-make-sure-it-is-in-your-library-path