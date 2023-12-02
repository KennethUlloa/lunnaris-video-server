
function createVideoElement(data) {
    let video = {
        videoId: data.mediaId,
        element: $.parseHTML(`<video src="/video/${data.mediaId}" controls class="video-player"/>`)[0],
        videoLastTime: 0.0,
        laterTime: 0
    }

    video.element.addEventListener('timeupdate', () => {
        if (Number.isNaN(video.element.currentTime)) {
            return;
        }
        
        let delta = video.videoLastTime - video.element.currentTime;
        if (Math.abs(delta) >= 10)  {
            video.videoLastTime = video.element.currentTime;
            let body =  new URLSearchParams();
            body.append('id',video.videoId);
            body.append('time',`${video.videoLastTime/video.element.duration}`);
            fetch('/api/media/watched', {
                method: 'put',
                body: body
            }).then(response => response.json())
            .then(d => console.log(d))
        }
    });

    return video;
}

