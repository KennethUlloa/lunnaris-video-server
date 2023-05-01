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
                    <span>
                        <i class="fa-solid fa-play play-button"></i>
                        Reproducir
                    </span>
                    <span>
                        <i class="fa-solid fa-backward-fast restart-button"></i>
                        Desde el inicio
                    </span>
                    
                </div>
            </div>
        </div>
    `;
    let element = $.parseHTML(content)[0];
    element.style.setProperty("--url",`url("../${data.thumb}")`);
    element.querySelector(".poster").style.setProperty("--b-url",`url("../${data.poster}")`);
    element.querySelector(".play-button").addEventListener('click', () => {
        let videoElement = $.parseHTML(`<div class="video-container">
        <video src="/video/${data.id}" controls class="video-player"/>
        </div>`)[0];
        setTopLayerContent(videoElement);
    });
    return element;

}