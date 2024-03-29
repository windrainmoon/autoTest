!function (t) {
    t.address = function () {
        var e, r, n = function (e) {
                var r = t.extend(t.Event(e), function () {
                    for (var e = {}, r = t.address.parameterNames(), n = 0, a = r.length; a > n; n++) e[r[n]] = t.address.parameter(r[n]);
                    return {
                        value: t.address.value(),
                        path: t.address.path(),
                        pathNames: t.address.pathNames(),
                        parameterNames: r,
                        parameters: e,
                        queryString: t.address.queryString()
                    }
                }.call(t.address));
                return t(t.address).trigger(r), r
            }, a = function (t) {
                return Array.prototype.slice.call(t)
            }, i = function () {
                return t().bind.apply(t(t.address), Array.prototype.slice.call(arguments)), t.address
            }, s = function () {
                return t().unbind.apply(t(t.address), Array.prototype.slice.call(arguments)), t.address
            }, o = function () {
                return B.pushState && L.state !== e
            }, c = function () {
                return ("/" + P.pathname.replace(new RegExp(L.state), "") + P.search + (u() ? "#" + u() : "")).replace(K, "/")
            }, u = function () {
                var t = P.href.indexOf("#");
                return -1 != t ? P.href.substr(t + 1) : ""
            }, d = function () {
                return o() ? c() : u()
            }, l = function () {
                try {
                    return top.document !== e && top.document.title !== e && top.jQuery !== e && top.jQuery.address !== e && top.jQuery.address.frames() !== !1 ? top : window
                } catch (t) {
                    return window
                }
            }, p = function () {
                return "javascript"
            }, h = function (t) {
                return t = t.toString(), (L.strict && "/" != t.substr(0, 1) ? "/" : "") + t
            }, f = function (t, e) {
                return parseInt(t.css(e), 10)
            }, g = function () {
                if (!Y) {
                    var t = d(), e = decodeURI(re) != decodeURI(t);
                    e && (W && 7 > C ? P.reload() : (W && !H && L.history && D(y, 50), re = t, v(O)))
                }
            }, v = function (t) {
                return D(m, 10), n(A).isDefaultPrevented() || n(t ? q : N).isDefaultPrevented()
            }, m = function () {
                if ("null" !== L.tracker && L.tracker !== I) {
                    var r = t.isFunction(L.tracker) ? L.tracker : _[L.tracker],
                        n = (P.pathname + P.search + (t.address && !o() ? t.address.value() : "")).replace(/\/\//, "/").replace(/^\/$/, "");
                    t.isFunction(r) ? r(n) : t.isFunction(_.urchinTracker) ? _.urchinTracker(n) : _.pageTracker !== e && t.isFunction(_.pageTracker._trackPageview) ? _.pageTracker._trackPageview(n) : _._gaq !== e && t.isFunction(_._gaq.push) && _._gaq.push(["_trackPageview", decodeURI(n)])
                }
            }, y = function () {
                var t = p() + ":" + O + ";document.open();document.writeln('<html><head><title>" + z.title.replace(/\'/g, "\\'") + "</title><script>var " + U + ' = "' + encodeURIComponent(d()).replace(/\'/g, "\\'") + (z.domain != P.hostname ? '";document.domain="' + z.domain : "") + "\";</script></head></html>');document.close();";
                7 > C ? r.src = t : r.contentWindow.location.replace(t)
            }, w = function () {
                if (J && -1 != V) {
                    var t, e, r = J.substr(V + 1).split("&");
                    for (t = 0; t < r.length; t++) e = r[t].split("="), /^(autoUpdate|history|strict|wrap)$/.test(e[0]) && (L[e[0]] = isNaN(e[1]) ? /^(true|yes)$/i.test(e[1]) : 0 !== parseInt(e[1], 10)), /^(state|tracker)$/.test(e[0]) && (L[e[0]] = e[1]);
                    J = I
                }
                re = d()
            }, b = function () {
                if (!Z) {
                    if (Z = $, w(), t('a[rel*="address:"]').address(), L.wrap) {
                        {
                            var a = t("body");
                            t("body > *").wrapAll('<div style="padding:' + (f(a, "marginTop") + f(a, "paddingTop")) + "px " + (f(a, "marginRight") + f(a, "paddingRight")) + "px " + (f(a, "marginBottom") + f(a, "paddingBottom")) + "px " + (f(a, "marginLeft") + f(a, "paddingLeft")) + 'px;" />').parent().wrap('<div id="' + U + '" style="height:100%;overflow:auto;position:relative;' + (M && !window.statusbar.visible ? "resize:both;" : "") + '" />')
                        }
                        t("html, body").css({
                            height: "100%",
                            margin: 0,
                            padding: 0,
                            overflow: "hidden"
                        }), M && t('<style type="text/css" />').appendTo("head").text("#" + U + "::-webkit-resizer { background-color: #fff; }")
                    }
                    if (W && !H) {
                        var i = z.getElementsByTagName("frameset")[0];
                        r = z.createElement((i ? "" : "i") + "frame"), r.src = p() + ":" + O, i ? (i.insertAdjacentElement("beforeEnd", r), i[i.cols ? "cols" : "rows"] += ",0", r.noResize = $, r.frameBorder = r.frameSpacing = 0) : (r.style.display = "none", r.style.width = r.style.height = 0, r.tabIndex = -1, z.body.insertAdjacentElement("afterBegin", r)), D(function () {
                            t(r).bind("load", function () {
                                var t = r.contentWindow;
                                re = t[U] !== e ? t[U] : "", re != d() && (v(O), P.hash = re)
                            }), r.contentWindow[U] === e && y()
                        }, 50)
                    }
                    D(function () {
                        n("init"), v(O)
                    }, 1), o() || (W && C > 7 || !W && H ? _.addEventListener ? _.addEventListener(R, g, O) : _.attachEvent && _.attachEvent("on" + R, g) : Q(g, 50)), "state" in window.history && t(window).trigger("popstate")
                }
            }, x = function () {
                decodeURI(re) != decodeURI(d()) && (re = d(), v(O))
            }, k = function () {
                _.removeEventListener ? _.removeEventListener(R, g, O) : _.detachEvent && _.detachEvent("on" + R, g)
            }, E = function (t) {
                t = t.toLowerCase();
                var e = /(chrome)[ \/]([\w.]+)/.exec(t) || /(webkit)[ \/]([\w.]+)/.exec(t) || /(opera)(?:.*version|)[ \/]([\w.]+)/.exec(t) || /(msie) ([\w.]+)/.exec(t) || t.indexOf("compatible") < 0 && /(mozilla)(?:.*? rv:([\w.]+)|)/.exec(t) || [];
                return {browser: e[1] || "", version: e[2] || "0"}
            }, S = function () {
                var t = {}, e = E(navigator.userAgent);
                return e.browser && (t[e.browser] = !0, t.version = e.version), t.chrome ? t.webkit = !0 : t.webkit && (t.safari = !0), t
            }, I = null, U = "jQueryAddress", j = "string", R = "hashchange", T = "init", A = "change",
            q = "internalChange", N = "externalChange", $ = !0, O = !1,
            L = {autoUpdate: $, history: $, strict: $, frames: $, wrap: O}, F = S(), C = parseFloat(F.version),
            M = F.webkit || F.safari, W = !t.support.opacity, _ = l(), z = _.document, B = _.history, P = _.location,
            Q = setInterval, D = setTimeout, K = /\/{2,9}/g, G = navigator.userAgent, H = "on" + R in _,
            J = t("script:last").attr("src"), V = J ? J.indexOf("?") : -1, X = z.title, Y = O, Z = O, te = $, ee = O,
            re = d();
        if (W) {
            C = parseFloat(G.substr(G.indexOf("MSIE") + 4)), z.documentMode && z.documentMode != C && (C = 8 != z.documentMode ? 7 : 8);
            var ne = z.onpropertychange;
            z.onpropertychange = function () {
                ne && ne.call(z), z.title != X && -1 != z.title.indexOf("#" + d()) && (z.title = X)
            }
        }
        if (B.navigationMode && (B.navigationMode = "compatible"), "complete" == document.readyState) var ae = setInterval(function () {
            t.address && (b(), clearInterval(ae))
        }, 50); else w(), t(b);
        return t(window).bind("popstate", x).bind("unload", k), {
            bind: function () {
                return i.apply(this, a(arguments))
            }, unbind: function () {
                return s.apply(this, a(arguments))
            }, init: function () {
                return i.apply(this, [T].concat(a(arguments)))
            }, change: function () {
                return i.apply(this, [A].concat(a(arguments)))
            }, internalChange: function () {
                return i.apply(this, [q].concat(a(arguments)))
            }, externalChange: function () {
                return i.apply(this, [N].concat(a(arguments)))
            }, baseURL: function () {
                var t = P.href;
                return -1 != t.indexOf("#") && (t = t.substr(0, t.indexOf("#"))), /\/$/.test(t) && (t = t.substr(0, t.length - 1)), t
            }, autoUpdate: function (t) {
                return t !== e ? (L.autoUpdate = t, this) : L.autoUpdate
            }, history: function (t) {
                return t !== e ? (L.history = t, this) : L.history
            }, state: function (t) {
                if (t !== e) {
                    L.state = t;
                    var r = c();
                    return L.state !== e && (B.pushState ? "/#/" == r.substr(0, 3) && P.replace(L.state.replace(/^\/$/, "") + r.substr(2)) : "/" != r && r.replace(/^\/#/, "") != u() && D(function () {
                        P.replace(L.state.replace(/^\/$/, "") + "/#" + r)
                    }, 1)), this
                }
                return L.state
            }, frames: function (t) {
                return t !== e ? (L.frames = t, _ = l(), this) : L.frames
            }, strict: function (t) {
                return t !== e ? (L.strict = t, this) : L.strict
            }, tracker: function (t) {
                return t !== e ? (L.tracker = t, this) : L.tracker
            }, wrap: function (t) {
                return t !== e ? (L.wrap = t, this) : L.wrap
            }, update: function () {
                return ee = $, this.value(re), ee = O, this
            }, title: function (t) {
                return t !== e ? (D(function () {
                    X = z.title = t, te && r && r.contentWindow && r.contentWindow.document && (r.contentWindow.document.title = t, te = O)
                }, 50), this) : z.title
            }, value: function (t) {
                if (t !== e) {
                    if (t = h(t), re == t && !ee) return;
                    if (re = t, L.autoUpdate || ee) {
                        if (v($)) return this;
                        o() ? B[L.history ? "pushState" : "replaceState"]({}, "", L.state.replace(/\/$/, "") + ("" === re ? "/" : re)) : (Y = $, M ? L.history ? P.hash = "#" + re : P.replace("#" + re) : re != d() && (L.history ? P.hash = "#" + re : P.replace("#" + re)), W && !H && L.history && D(y, 50), M ? D(function () {
                            Y = O
                        }, 1) : Y = O)
                    }
                    return this
                }
                return h(re)
            }, path: function (t) {
                if (t !== e) {
                    var r = this.queryString(), n = this.hash();
                    return this.value(t + (r ? "?" + r : "") + (n ? "#" + n : "")), this
                }
                return h(re).split("#")[0].split("?")[0]
            }, pathNames: function () {
                var t = this.path(), e = t.replace(K, "/").split("/");
                return ("/" == t.substr(0, 1) || 0 === t.length) && e.splice(0, 1), "/" == t.substr(t.length - 1, 1) && e.splice(e.length - 1, 1), e
            }, queryString: function (t) {
                if (t !== e) {
                    var r = this.hash();
                    return this.value(this.path() + (t ? "?" + t : "") + (r ? "#" + r : "")), this
                }
                var n = re.split("?");
                return n.slice(1, n.length).join("?").split("#")[0]
            }, parameter: function (r, n, a) {
                var i, s;
                if (n !== e) {
                    var o = this.parameterNames();
                    for (s = [], n = n === e || n === I ? "" : n.toString(), i = 0; i < o.length; i++) {
                        var c = o[i], u = this.parameter(c);
                        typeof u == j && (u = [u]), c == r && (u = n === I || "" === n ? [] : a ? u.concat([n]) : [n]);
                        for (var d = 0; d < u.length; d++) s.push(c + "=" + u[d])
                    }
                    return -1 == t.inArray(r, o) && n !== I && "" !== n && s.push(r + "=" + n), this.queryString(s.join("&")), this
                }
                if (n = this.queryString()) {
                    var l = [];
                    for (s = n.split("&"), i = 0; i < s.length; i++) {
                        var p = s[i].split("=");
                        p[0] == r && l.push(p.slice(1).join("="))
                    }
                    if (0 !== l.length) return 1 != l.length ? l : l[0]
                }
            }, parameterNames: function () {
                var e = this.queryString(), r = [];
                if (e && -1 != e.indexOf("=")) for (var n = e.split("&"), a = 0; a < n.length; a++) {
                    var i = n[a].split("=")[0];
                    -1 == t.inArray(i, r) && r.push(i)
                }
                return r
            }, hash: function (t) {
                if (t !== e) return this.value(re.split("#")[0] + (t ? "#" + t : "")), this;
                var r = re.split("#");
                return r.slice(1, r.length).join("#")
            }
        }
    }(), t.fn.address = function (e) {
        return t(this).each(function () {
            t(this).data("address") || t(this).on("click", function (r) {
                if (r.shiftKey || r.ctrlKey || r.metaKey || 2 == r.which) return !0;
                var n = r.currentTarget;
                if (t(n).is("a")) {
                    r.preventDefault();
                    var a = e ? e.call(n) : /address:/.test(t(n).attr("rel")) ? t(n).attr("rel").split("address:")[1].split(" ")[0] : void 0 === t.address.state() || /^\/?$/.test(t.address.state()) ? t(n).attr("href").replace(/^(#\!?|\.)/, "") : t(n).attr("href").replace(new RegExp("^(.*" + t.address.state() + "|\\.)"), "");
                    t.address.value(a)
                }
            }).on("submit", function (r) {
                var n = r.currentTarget;
                if (t(n).is("form")) {
                    r.preventDefault();
                    var a = t(n).attr("action"),
                        i = e ? e.call(n) : (-1 != a.indexOf("?") ? a.replace(/&$/, "") : a + "?") + t(n).serialize();
                    t.address.value(i)
                }
            }).data("address", !0)
        }), this
    }
}(jQuery);