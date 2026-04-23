function get_a(page) {
    function randomStr(e) {
        for (var t = [], n = 0; n < e; n++)
            t.push(this.random(0, 35).toString(36));
        return t.join("")
    }

    random = function (e, t) {
        return void 0 === e && (e = 0),
        void 0 === t && (t = 1e4),
            Math.round(Math.random() * (t - e) + e)
    }

    function uuid(t, n) {
        void 0 === t && (t = 16),
        void 0 === n && (n = !1),
        !n && t < 16 && (console.error("uuid useCase=false 时 len 不能小于 16"),
            t = 16),
        n && t < 12 && (console.error("uuid useCase=true 时 len 不能小于 12"),
            t = 12);
        var i = ((new Date).getTime() + 1e14).toString();
        return i += ("000" + (++e.uuidCount).toString()).substr(-3, 3),
            i = n ? parseInt(i).to62() : parseInt(i).toString(36),
            i += randomStr(t),
            i = i.substr(0, t),
            i
    }

    function e(e, t, n) {
        this.list = [],
            this.idle = !0,
            this.clientKey = uuid(16, null),
            this.opt = e,
            this.dc = t,
        n && (this.clientKey = n)
    }

    // e = new e
    var o = {
        "id": uuid(16, null),
        "projectKey": "honsan_cloud_ccprec",
        "clientKey": uuid(16, null),
        "token": null,
        "clientDailyData": {},
        "acts": [
            {
                "id": "rtumoqunlbk7k53m",
                "fullPath": "/ccprec.com.cn.web/client/info/cqweb_nonphy_cqzr",
                "args": [
                    page,
                    20,
                    null
                ]
            }
        ]
    }
   return  JSON.stringify(o)
}

// console.log(get_a())