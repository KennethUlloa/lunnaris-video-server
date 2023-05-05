const time_setted_ev = new CustomEvent("timesetted");


function poster(data) {
    let content = `<div class="poster-wrapper">
        <div class="poster-container" tabindex="0">
            <div class="poster hoverable" style="--b-url: url(\"${data.poster}\")">
                <img src="${data.poster}">
                <button class="btn"><i class="fa-solid fa-play"></i></button>
            </div>
            <h4 class="title">${data.title}</h4>
        </div>
    </div>`;
    let element = $.parseHTML(content)[0];
    element.querySelector(".poster").style.setProperty("--b-url",`url("../${data.poster}")`);
    element.addEventListener('click', () => {
        setTopLayerContent(preview(data));
        showTopLayer();
    });
    return element;
}

function setTopLayerContent(content) {
    $("#top-layer-content").empty();
    $("#top-layer-content").append(content);
}

function showTopLayer() {
    $("#top-layer").removeClass("ln-d-none-i");
}

function hideTopLayer() {
    $("#top-layer-content").empty();
    $("#top-layer").addClass("ln-d-none-i");
    document.title = 'Lunnaris Server';
}

function preview(data) {
    let content = `<div class="preview-container ln-md-br-0-i ln-md-w-100 ln-md-h-100 ln-md-flex-column ln-md-ai-center">
            <div class="poster">
                <img src="${data.poster}">
            </div>
            <div class="preview-panel">
                <h2>${data.title}</h2>
                <div class="ln-flex-row ln-my-3">
                    <span>${data.year}</span>
                    ${data.genre.map(g => `<span class="ln-mx-2">${g}</span>`).join('<span class="separator v"></span>')}
                </div>
                <p>${data.sinopsys}</p>
                <div class="view-progress ln-my-3"></div>
                <div class="preview-controls">
                    <span class="disabled play-button">
                        <i class="fa-solid fa-play"></i>
                        Reproducir
                    </span>
                    <span class="restart-button">
                        <i class="fa-solid fa-backward-fast"></i>
                        Desde el inicio
                    </span>
                    
                </div>
            </div>
        </div>
    `;
    let videoElement;
    let time = 0;
    let element = $.parseHTML(content)[0];
    element.style.setProperty("--url",`url("../${data.thumb}")`);
    element.querySelector(".poster").style.setProperty("--b-url",`url("../${data.poster}")`);
    element.querySelector(".restart-button").addEventListener('click', () => {
        videoElement = createVideoElement(data);
        setTopLayerContent(videoElement.element);
    });
    

    fetch(`/api/media/${data.id}`)
    .then(response => response.json())
    .then(response => {
        time = response.time;
        element.querySelector('.view-progress').style.setProperty('--progress',`${response.time}`)
        element.querySelector(".play-button").addEventListener('click', () => {
            videoElement = createVideoElement(data);
            videoElement.element.addEventListener('loadedmetadata', () => {
                videoElement.element.currentTime = time * videoElement.element.duration;
            });
            document.title = `Reproduciendo: ${data.title}`;
            setTopLayerContent(videoElement.element);
        });
        element.querySelector(".play-button").classList.toggle('disabled', false);
    });
    return element;

}