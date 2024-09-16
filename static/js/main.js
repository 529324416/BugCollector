let app = {
    "currentMainUrl": null,
    "lastMenu": null,
    "reloadMain": function(){},
}

const _loading = '<span id="__spec__loading_anim" class="loading loading-spinner loading-md"></span>'

function reload_main()
{
    if(app.reloadMain != null)
    {
        app.reloadMain()
    }
}

/* 关于主页控制 */
function load_main(url)
{
    /* 加载主页内容 */
    fetch(url)
        .then(response => response.text())
        .then(data => {
            app.reloadMain = function(){ load_main(url); }
            document.getElementById('MainContent').innerHTML = data;
        });
}

function load_main_cb(url, cb)
{
    /* 加载主页内容 */
    fetch(url)
        .then(response => response.text())
        .then(data => {
            app.reloadMain = function(){ load_main_cb(url, cb); }
            document.getElementById('MainContent').innerHTML = data;
            cb();
        });
}

function load_main_with_chart(url, chartUrl, chartId)
{
    /* 加载主页内容 */
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById('MainContent').innerHTML = data;
            __load_echart(chartUrl, chartId);
            app.reloadMain = function(){ load_main_with_chart(url, chartUrl, chartId); }
        });
}

function __load_echart(url, id)
{
    /* fetch data from url and initialize echar to canvas id */
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var host = document.getElementById(id);
            if(host == null) return;
            var theme = document.documentElement.getAttribute('data-theme');
            var chartTheme = theme == "dark" ? "daisyui_dark" : "light";
            var chart = echarts.init(host, chartTheme);
            chart.setOption(data);
        });
}

// function load_sidemenu(url){
//     fetch(url)
//         .then(response => response.text())
//         .then(data => {
//             document.getElementById('SideMenu').innerHTML = data;
//         });
// }

// function load_sidemenu_cb(url, cb){
//     fetch(url)
//         .then(response => response.text())
//         .then(data => {
//             document.getElementById('SideMenu').innerHTML = data;
//             cb();
//         });
// }

function load_titlebar(url){
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById('HeadBar').innerHTML = data;
        });
}

// function bug_exception_load(id, url)
// {
//     var checkbox = document.getElementById(id)
//     if(checkbox == null) return;
//     if(checkbox.checked){
//         load_main(url+"?handled=false")
//     }else{
//         load_main(url)
//     }
// }

function bug_exception_update_handle_status(url, data_id, value)
{
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': data_id,
            'handled': value
        })
    }).then(response => response.json())
    .then(data => {
        reload_main();
    });
}

function update_theme_now()
{
    var currentTheme = document.documentElement.getAttribute('data-theme');
    var _theme = "dark"
    if(currentTheme == 'dark')
    {
        _theme = "wireframe";
    }
    document.documentElement.setAttribute('data-theme', _theme);
    fetch('/utils/set_theme/' + _theme)
        // .then(response => response.json())
        .then(data => {
            reload_main();
        });
}

function mark_menu_status(elementId, classAttr)
{
    var element = document.getElementById(elementId);
    if(element == null) return;

    if(app.lastMenu != null)
    {
        app.lastMenu.classList.remove(classAttr);
    }
    element.classList.add(classAttr);
    app.lastMenu = element;
}

function add_loading_anim(id)
{
    var element = document.getElementById(id);
    if(element == null) return;
    element.innerHTML += _loading;
}

function remove_loading_anim(id)
{
    var element = document.getElementById(id);
    if(element == null) return;
    element.innerHTML = element.innerHTML.replace(_loading, "");
}