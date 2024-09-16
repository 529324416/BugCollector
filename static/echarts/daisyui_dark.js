(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['exports', 'echarts'], factory);
    } else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {
        // CommonJS
        factory(exports, require('echarts'));
    } else {
        // Browser globals
        factory({}, root.echarts);
    }
}(this, function (exports, echarts) {
    var log = function (msg) {
        if (typeof console !== 'undefined') {
            console && console.error && console.error(msg);
        }
    };
    if (!echarts) {
        log('ECharts is not Loaded');
        return;
    }
    echarts.registerTheme('daisyui_dark', {
        "color": [
            "#7582ff",
            "#ff71cf",
            "#00c7b5",
            "#00ca92",
            "#ffc22d",
            "#a4d8c2",
            "#ff6f70",
            "#d3758f",
            "#dcc392",
            "#2e4783",
            "#82b6e9",
            "#ff6347",
            "#a092f1",
            "#0a915d",
            "#eaf889",
            "#6699FF",
            "#ff6666",
            "#3cb371",
            "#d5b158",
            "#38b6b6"
        ],
        "backgroundColor": "rgba(25,30,36,1)",
        "textStyle": {},
        "title": {
            "textStyle": {
                "color": "#a6adbb"
            },
            "subtextStyle": {
                "color": "#a6adbb"
            }
        },
        "line": {
            "itemStyle": {
                "borderWidth": 1
            },
            "lineStyle": {
                "width": 2
            },
            "symbolSize": 4,
            "symbol": "rect",
            "smooth": true
        },
        "radar": {
            "itemStyle": {
                "borderWidth": 1
            },
            "lineStyle": {
                "width": 2
            },
            "symbolSize": 4,
            "symbol": "rect",
            "smooth": true
        },
        "bar": {
            "itemStyle": {
                "barBorderWidth": "0",
                "barBorderColor": "rgba(204,204,204,0)"
            }
        },
        "pie": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            }
        },
        "scatter": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            }
        },
        "boxplot": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            }
        },
        "parallel": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            }
        },
        "sankey": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            }
        },
        "funnel": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            }
        },
        "gauge": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            }
        },
        "candlestick": {
            "itemStyle": {
                "color": "#e01f54",
                "color0": "#001852",
                "borderColor": "#f5e8c8",
                "borderColor0": "#b8d2c7",
                "borderWidth": 1
            }
        },
        "graph": {
            "itemStyle": {
                "borderWidth": "0",
                "borderColor": "rgba(204,204,204,0)"
            },
            "lineStyle": {
                "width": 1,
                "color": "#aaaaaa"
            },
            "symbolSize": 4,
            "symbol": "rect",
            "smooth": true,
            "color": [
                "#7582ff",
                "#ff71cf",
                "#00c7b5",
                "#00ca92",
                "#ffc22d",
                "#a4d8c2",
                "#ff6f70",
                "#d3758f",
                "#dcc392",
                "#2e4783",
                "#82b6e9",
                "#ff6347",
                "#a092f1",
                "#0a915d",
                "#eaf889",
                "#6699FF",
                "#ff6666",
                "#3cb371",
                "#d5b158",
                "#38b6b6"
            ],
            "label": {
                "color": "#fffde3"
            }
        },
        "map": {
            "itemStyle": {
                "areaColor": "#eeeeee",
                "borderColor": "#444444",
                "borderWidth": 0.5
            },
            "label": {
                "color": "#000000"
            },
            "emphasis": {
                "itemStyle": {
                    "areaColor": "rgba(255,215,0,0.8)",
                    "borderColor": "#444",
                    "borderWidth": 1
                },
                "label": {
                    "color": "rgb(100,0,0)"
                }
            }
        },
        "geo": {
            "itemStyle": {
                "areaColor": "#eeeeee",
                "borderColor": "#444444",
                "borderWidth": 0.5
            },
            "label": {
                "color": "#000000"
            },
            "emphasis": {
                "itemStyle": {
                    "areaColor": "rgba(255,215,0,0.8)",
                    "borderColor": "#444",
                    "borderWidth": 1
                },
                "label": {
                    "color": "rgb(100,0,0)"
                }
            }
        },
        "categoryAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "rgba(92,93,95,0.58)"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#a6adbb"
                }
            },
            "axisLabel": {
                "show": true,
                "color": "#a6adbb"
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "rgba(204,204,204,0.27)",
                        "rgba(204,204,204,0.27)",
                        "rgba(204,204,204,0.27)"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "rgba(250,250,250,0.3)",
                        "rgba(200,200,200,0.3)"
                    ]
                }
            }
        },
        "valueAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "rgba(104,104,104,0.21)"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#a6adbb"
                }
            },
            "axisLabel": {
                "show": true,
                "color": "#a6adbb"
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "rgba(101,101,101,0.38)"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "rgba(250,250,250,0.3)",
                        "rgba(200,200,200,0.3)"
                    ]
                }
            }
        },
        "logAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "#a6adbb"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#a6adbb"
                }
            },
            "axisLabel": {
                "show": true,
                "color": "#a6adbb"
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "#a6adbb"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "rgba(250,250,250,0.3)",
                        "rgba(200,200,200,0.3)"
                    ]
                }
            }
        },
        "timeAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "#a6adbb"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#a6adbb"
                }
            },
            "axisLabel": {
                "show": true,
                "color": "#a6adbb"
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "#a6adbb"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "rgba(250,250,250,0.3)",
                        "rgba(200,200,200,0.3)"
                    ]
                }
            }
        },
        "toolbox": {
            "iconStyle": {
                "borderColor": "#a6adbb"
            },
            "emphasis": {
                "iconStyle": {
                    "borderColor": "#a6adbb"
                }
            }
        },
        "legend": {
            "textStyle": {
                "color": "#a6adbb"
            }
        },
        "tooltip": {
            "axisPointer": {
                "lineStyle": {
                    "color": "#a6adbb",
                    "width": "1"
                },
                "crossStyle": {
                    "color": "#a6adbb",
                    "width": "1"
                }
            }
        },
        "timeline": {
            "lineStyle": {
                "color": "#293c55",
                "width": "1"
            },
            "itemStyle": {
                "color": "#a6adbb",
                "borderWidth": "0"
            },
            "controlStyle": {
                "color": "#293c55",
                "borderColor": "#293c55",
                "borderWidth": "1"
            },
            "checkpointStyle": {
                "color": "#e43c59",
                "borderColor": "#c23531"
            },
            "label": {
                "color": "#293c55"
            },
            "emphasis": {
                "itemStyle": {
                    "color": "#a9334c"
                },
                "controlStyle": {
                    "color": "#293c55",
                    "borderColor": "#293c55",
                    "borderWidth": "1"
                },
                "label": {
                    "color": "#293c55"
                }
            }
        },
        "visualMap": {
            "color": [
                "#e01f54",
                "#e7dbc3"
            ]
        },
        "dataZoom": {
            "backgroundColor": "rgba(47,69,84,0)",
            "dataBackgroundColor": "rgba(47,69,84,0.3)",
            "fillerColor": "rgba(167,183,204,0.4)",
            "handleColor": "#a7b7cc",
            "handleSize": "100%",
            "textStyle": {
                "color": "#333333"
            }
        },
        "markPoint": {
            "label": {
                "color": "#fffde3"
            },
            "emphasis": {
                "label": {
                    "color": "#fffde3"
                }
            }
        }
    });
}));
