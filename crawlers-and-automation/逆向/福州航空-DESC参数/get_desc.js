const CryptoJS = require('crypto-js');
const {JSDOM} = require("jsdom");
const dom = new JSDOM(`
<!DOCTYPE html>
<html>
  <body>
    <div id="app">hello</div>
  </body>
</html>
`)
const {des_decrypt: _0x58990f} = require('./DES_encrypt')
window = dom.window;
Object.defineProperty(window.screen, 'colorDepth', {
    configurable: true,
    get: () => 32
});

document = dom.window.document;

navigator = dom.window.navigator;
navigator.language = "zh-CN"
navigator.platform = 'Win32'
navigator.doNotTrack = null
Object.defineProperty(navigator, 'userAgent', {
    get: () => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    configurable: true
});

function get_desc() {
    var _0x2e185c = [];
    _0x2e185c["push"](navigator["userAgent"])
    _0x2e185c["push"](navigator["language"])
    _0x2e185c['push'](window.screen["colorDepth"])
    _0x2e185c["push"](new Date()["getTimezoneOffset"]())
    _0x2e185c["push"](true)
    _0x2e185c['push'](true)
    _0x2e185c['push'](true)
    _0x2e185c['push']("undefined")
    _0x2e185c['push']("undefined")
    _0x2e185c["push"]('cpuClass:' + 'undefined')
    _0x2e185c["push"]('platform:' + navigator['platform'])
    _0x2e185c['push']("doNotTrack:" + navigator["doNotTrack"])
    _0x2e185c["push"]('Plugin:' + "PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf")
    _0x2e185c['push']('1')
    _0x2e185c["push"]('0') //是否nodejs
    _0x2e185c["push"]('0') //是否自动化
    _0x2e185c['push']('0') //是否PhantomJS
    _0x2e185c["push"]('0') //是否无头浏览器
    _0x2e185c['push']("Netscape&getBattery&8&20&Gecko&20030107")
    _0x2e185c['push']('0') //是否火狐
    _0x2e185c["push"]('0') //是否safari
    _0x2e185c['push']("Netscape&Google Inc.")
    _0x2e185c["push"]("59bf7b14")

    console.log(_0x2e185c)


    function words_hash3_32_gc(_0xde91c, _0x3b08af) {
        var _0x6264b8, _0x232116, _0xa0a6ab, _0x16d2fe, _0x12f8c5, _0x2b6af4, _0x58aa6b, _0x394534;
        for (_0x6264b8 = 0x3 & _0xde91c["length"],
                 _0x232116 = _0xde91c["length"] - _0x6264b8,
                 _0xa0a6ab = _0x3b08af,
                 _0x12f8c5 = 0xcc9e2d51,
                 _0x2b6af4 = 0x1b873593,
                 _0x394534 = 0x0; _0x232116 > _0x394534;)
            _0x58aa6b = 0xff & _0xde91c['charCodeAt'](_0x394534) | (0xff & _0xde91c['charCodeAt'](++_0x394534)) << 0x8 | (0xff & _0xde91c["charCodeAt"](++_0x394534)) << 0x10 | (0xff & _0xde91c['charCodeAt'](++_0x394534)) << 0x18,
                ++_0x394534,
                _0x58aa6b = (0xffff & _0x58aa6b) * _0x12f8c5 + (((_0x58aa6b >>> 0x10) * _0x12f8c5 & 0xffff) << 0x10) & 0xffffffff,
                _0x58aa6b = _0x58aa6b << 0xf | _0x58aa6b >>> 0x11,
                _0x58aa6b = (0xffff & _0x58aa6b) * _0x2b6af4 + (((_0x58aa6b >>> 0x10) * _0x2b6af4 & 0xffff) << 0x10) & 0xffffffff,
                _0xa0a6ab ^= _0x58aa6b,
                _0xa0a6ab = _0xa0a6ab << 0xd | _0xa0a6ab >>> 0x13,
                _0x16d2fe = 0x5 * (0xffff & _0xa0a6ab) + ((0x5 * (_0xa0a6ab >>> 0x10) & 0xffff) << 0x10) & 0xffffffff,
                _0xa0a6ab = (0xffff & _0x16d2fe) + 0x6b64 + (((_0x16d2fe >>> 0x10) + 0xe654 & 0xffff) << 0x10);
        switch (_0x58aa6b = 0x0,
            _0x6264b8) {
            case 0x3:
                _0x58aa6b ^= (0xff & _0xde91c["charCodeAt"](_0x394534 + 0x2)) << 0x10;
            case 0x2:
                _0x58aa6b ^= (0xff & _0xde91c['charCodeAt'](_0x394534 + 0x1)) << 0x8;
            case 0x1:
                _0x58aa6b ^= 0xff & _0xde91c["charCodeAt"](_0x394534),
                    _0x58aa6b = (0xffff & _0x58aa6b) * _0x12f8c5 + (((_0x58aa6b >>> 0x10) * _0x12f8c5 & 0xffff) << 0x10) & 0xffffffff,
                    _0x58aa6b = _0x58aa6b << 0xf | _0x58aa6b >>> 0x11,
                    _0x58aa6b = (0xffff & _0x58aa6b) * _0x2b6af4 + (((_0x58aa6b >>> 0x10) * _0x2b6af4 & 0xffff) << 0x10) & 0xffffffff,
                    _0xa0a6ab ^= _0x58aa6b;
        }
        return _0xa0a6ab ^= _0xde91c["length"],
            _0xa0a6ab ^= _0xa0a6ab >>> 0x10,
            _0xa0a6ab = 0x85ebca6b * (0xffff & _0xa0a6ab) + ((0x85ebca6b * (_0xa0a6ab >>> 0x10) & 0xffff) << 0x10) & 0xffffffff,
            _0xa0a6ab ^= _0xa0a6ab >>> 0xd,
            _0xa0a6ab = 0xc2b2ae35 * (0xffff & _0xa0a6ab) + ((0xc2b2ae35 * (_0xa0a6ab >>> 0x10) & 0xffff) << 0x10) & 0xffffffff,
            _0xa0a6ab ^= _0xa0a6ab >>> 0x10,
        _0xa0a6ab >>> 0x0;
    }

    var _0x5d4576 = words_hash3_32_gc(_0x2e185c['join']('###'), 0x1f);
    console.log(_0x5d4576)

    var _0x51c9b1 = '59bf7b14' + '#' +
        CryptoJS.MD5(_0x5d4576 + "you are good!" + Math['floor'](Math["random"]() * 0xa)["toString"]()).toString(CryptoJS.enc.Hex)["substring"](0x18) + '#' +
        "Netscape&Google Inc." + '#' +
        "0" + '#' +
        "0" + '#' +
        "Netscape&getBattery&8&20&Gecko&20030107" + '#' +
        "0" + '#' +
        "0" + '#' +
        "0" + '#' +
        "0" + '#' +
        [1080, 1920] + '#' +
        "20210715" + '#' +
        false + '#' +
        true + '#' +
        true + '#' +
        true + '#' +
        "59bf7b14" + "20210715" + "59bf7b14";

    console.log(_0x51c9b1)
    var _0x28c10a = {
        'xy': [],
        'fingerprint': _0x5d4576,
        'prevent_pev': null,
        'prevent_cid': _0x51c9b1,
        't': new Date()['valueOf']()
    }

    function _0x4f2b66(_0x509b5f, _0x129914, _0xcbf4a9) {
        var _0x34478a = new RegExp(_0x129914, 'g');
        return words = _0x509b5f["replace"](_0x34478a, _0xcbf4a9),
            words;
    }

    function _0x3306bb(_0x4b9529, _0x3b136c) {
        var _0x4ca506 = _0x58990f["enc"]["Utf8"]["parse"](_0x3b136c)
            , _0x55d6fd = _0x58990f["DES"]['encrypt'](_0x4b9529, _0x4ca506, {
            'mode': _0x58990f['mode']['CBC'],
            'padding': _0x58990f['pad']["Nopk"]
        });
        return _0x4f2b66(_0x55d6fd['toString'](), '\x5c+', '%2B');
    }

    var _0x1e22d3 = JSON['stringify'](_0x28c10a);
    var _0x284636 = _0x3306bb(_0x1e22d3, "52D2841A3485DFFBCF2EA6A0515077CD");

    return _0x284636
}

console.log(get_desc())