function loadContent(url) {
    fetch(url).then(response => response.text()).then(html => {
        document.querySelector('main').innerHTML = html;
    });
}