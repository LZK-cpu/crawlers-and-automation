window = global;
window.outerHeight = 1032
window.innerHeight = 722
window.outerWidth = 1920
window.innerHeight = 1912

location = {
    href: "https://www.dingxiang-inc.com/business/captcha",
}

function Navigator() {
}

Navigator.prototype.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
Navigator.prototype.platform = "Win32"
var navigator = new Navigator();
Object.defineProperty(global, 'navigator', {
    value: navigator,
    configurable: true
});
window.navigator = navigator;
document = {
    "referrer": "",
    "documentElement": {
        "doScroll": undefined,
        "getAttribute": function (arg) {
            return null
        },
        'clientWidth': 1912,
        'clientHeight': 722
    },
    'body': {
        'clientWidth': 1897,
        'clientHeight': 722
    },
    "getElementsByTagName": function (arg) {
        return {"0": {}, "1": {}, "2": {}, "3": {}, "4": {}, "5": {}, "6": {}, "7": {}, "8": {}}
    }
}

var screen = function () {
}
screen.prototype.width = 1920;
screen.prototype.height = 1080;
screen.prototype.availWidth = 1920;
screen.prototype.availHeight = 1032;
screen.prototype.colorDepth = 24;
window.screen = new screen();