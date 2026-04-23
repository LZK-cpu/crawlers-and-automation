require('./env.js')
require('./main.js')

// require('./de.js')

function before_track(sid) {
    xxx = window._dx['UA']['init']({})
    xxx.__proto__.ua = ""
    xxx.__proto__._ua = []
    xxx.__proto__.option = {
        "token": sid,
        "form": ""
    }
    console.log("sid", sid)
    xxx.__proto__.getTK()
    xxx.__proto__.getSC()
    xxx.__proto__._sa = []
    xxx.__proto__._ca = []
}


function random_randint(min, max) {
    var range = max - min;
    var rand = Math.random();
    var num = min + Math.round(rand * range);
    return num;
}

function slide_track(start, end) {
    function __ease_out_expo(sep) {
        if (sep == 1) {
            return 1
        } else {
            return 1 - Math.pow(2, -10 * sep)
        }
    }

    var slide_track = [
        [start[0], end[1], 3500]
    ]
    var count = parseInt(end[0] / 2)
    var t = random_randint(50, 100)
    var _x = 0,
        _y = 0
    for (i = 0; i < count; i++) {
        var x = Math.round(__ease_out_expo(i / count) * end[0])
        var t = t + random_randint(30, 50)
        if (x == _x) {
            continue
        }
        slide_track.push([start[0] + x, start[1] + _y, 3500 + t])
        _x = x
    }
    return slide_track
}

function click_track(click_list) {
    var t = random_randint(50, 100)
    for (let i = 0; i < click_list.length; i++) {
        var t = t + random_randint(30, 50)
        click_list[i][2] = 3500 + t
    }
    return click_list
}

function puzzle_track(start, end) {

    function __ease_out_expo(sep) {
        if (sep === 1) {
            return 1;
        } else {
            return 1 - Math.pow(2, -10 * sep);
        }
    }

    var slide_track = [
        [start[0], start[1], 3500]
    ];

    var count = 30;

    var t = Math.floor(Math.random() * 50 + 50);

    var _x = start[0];
    var _y = start[1];

    var dx = end[0] - start[0];
    var dy = end[1] - start[1];

    for (var i = 1; i <= count; i++) {

        var sep = i / count;

        var ease = __ease_out_expo(sep);

        var x = Math.round(start[0] + dx * ease);
        var y = Math.round(start[1] + dy * ease);

        t += Math.floor(Math.random() * 30 + 20);

        if (x === _x && y === _y) {
            continue;
        }

        slide_track.push([x, y, 3500 + t]);

        _x = x;
        _y = y;
    }

    return slide_track;
}

function get_ac_slide(sid, start, end) {
    before_track(sid)
    mousemove = slide_track([400, 500], end)
    console.log(xxx.__proto__.ua)
    console.log(mousemove)
    for (i = 0; i < mousemove.length; i++) {
        xxx.__proto__.tm = new Date().getTime() - mousemove[i][2]
        xxx.__proto__.recordSA({
            "pageX": mousemove[i][0],
            "pageY": mousemove[i][1]
        })
    }
    xxx.__proto__.sendSA()
    xxx.__proto__.sendTemp({
        "xpath": "/html/body/div[10]",
        "x": end[0],
        "y": end[1]
    })
    return xxx.__proto__.ua
}

function get_ac_click_track(sid, click_list) {
    before_track(sid)
    click_track(click_list)
    console.log(xxx.__proto__.ua)
    console.log(click_list)
    for (i = 0; i < click_list.length; i++) {
        xxx.__proto__.tm = new Date().getTime() - click_list[i][2]
        xxx.__proto__.recordCA({
            "offsetX": click_list[i][0],
            "offsetY": click_list[i][1],
            'target': {'className': 'dx_captcha_clickword_hits'}
        })
    }
    xxx.__proto__.sendCA()
    xxx.__proto__.sendTemp({
        "xpath": "/html/body/div[10]",
    })
    return xxx.__proto__.ua
}

function get_ac_one_click(sid, point) {
    before_track(sid)
    xxx.__proto__.recordCA({
        "offsetX": point[0],
        "offsetY": point[1],
        'target': {'className': 'dx_captcha_clickword_hits'}
    })
    xxx.__proto__.sendSA()
    xxx.__proto__.sendTemp({
        "xpath": "/html/body/div[10]",
        'x': point[0],
        'y': point[1]
    })
    return xxx.__proto__.ua
}

function get_ac_puzzle_move(sid, start, end, orders) {
    before_track(sid)
    mousemove = puzzle_track(start, end)
    orders = orders.join(',')
    console.log(xxx.__proto__.ua)
    console.log(mousemove)
    for (i = 0; i < mousemove.length; i++) {
        xxx.__proto__.tm = new Date().getTime() - mousemove[i][2]
        xxx.__proto__.recordSA({
            "pageX": mousemove[i][0],
            "pageY": mousemove[i][1]
        })
    }
    xxx.__proto__.sendSA()
    xxx.__proto__.sendTemp({
        "xpath": "/html/body/div[10]",
        'orders': orders
    })
    return xxx.__proto__.ua
}

console.log(get_ac_slide('5335a16567fbfcce56e731a9e6ba4aba', [100, 100], [300, 800]))
// console.log(get_ac_click_4('5335a16567fbfcce56e731a9e6ba4aba', [[77, 42], [45, 104], [158, 39], [99, 105]]))
// console.log(get_ac_one_click('5335a16567fbfcce56e731a9e6ba4aba', [77, 42]))