(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-5d632024"],{"17dc":function(e,t,n){"use strict";n("b0c0");var o=n("7a23"),i=Object(o["K"])("data-v-38eb9831");Object(o["u"])("data-v-38eb9831");var c={class:"name col-l-10 col-m-9 col-s-8"},a=Object(o["h"])("i",{class:"fa fa-info"},null,-1),r={class:"toggler col-l-2 col-m-3 col-s-4"};Object(o["s"])();var s=i((function(e,t,n,i,s,u){var l=Object(o["z"])("Loading"),f=Object(o["z"])("ToggleSwitch");return Object(o["r"])(),Object(o["e"])("div",{class:"switch",onClick:t[2]||(t[2]=Object(o["J"])((function(){return u.onToggle&&u.onToggle.apply(u,arguments)}),["stop"]))},[n.loading?(Object(o["r"])(),Object(o["e"])(l,{key:0})):Object(o["f"])("",!0),Object(o["h"])("div",c,[n.hasInfo?(Object(o["r"])(),Object(o["e"])("button",{key:0,onClick:t[1]||(t[1]=Object(o["J"])((function(){return u.onInfo&&u.onInfo.apply(u,arguments)}),["prevent"]))},[a])):Object(o["f"])("",!0),Object(o["h"])("span",{class:"name-content",textContent:Object(o["C"])(n.name)},null,8,["textContent"])]),Object(o["h"])("div",r,[Object(o["h"])(f,{disabled:n.loading,value:n.state,onInput:u.onToggle},null,8,["disabled","value","onInput"])])])})),u=n("0279"),l=n("3a5e"),f={name:"Switch",components:{Loading:l["a"],ToggleSwitch:u["a"]},emits:["toggle","info"],props:{name:{type:String,required:!0},state:{type:Boolean,default:!1},loading:{type:Boolean,default:!1},hasInfo:{type:Boolean,default:!1},id:{type:String}},methods:{onInfo:function(e){return e.stopPropagation(),this.$emit("info"),!1},onToggle:function(e){return e.stopPropagation(),this.$emit("toggle"),!1}}};n("fe3c");f.render=s,f.__scopeId="data-v-38eb9831";t["a"]=f},"43ec":function(e,t,n){},"487b":function(e,t,n){"use strict";var o=n("1da1"),i=(n("b0c0"),n("96cf"),n("3e54")),c={name:"SwitchesMixin",mixins:[i["a"]],props:{pluginName:{type:String,required:!0},bus:{type:Object,required:!0},config:{type:Object,default:function(){return{}}},selected:{type:Boolean,default:!1}},data:function(){return{loading:!1,initialized:!1,selectedDevice:null,devices:{}}},methods:{onRefreshEvent:function(e){e===this.pluginName&&this.refresh()},toggle:function(e,t){var n=this;return Object(o["a"])(regeneratorRuntime.mark((function o(){var i;return regeneratorRuntime.wrap((function(o){while(1)switch(o.prev=o.next){case 0:return null==t&&(t=e),o.next=3,n.request("".concat(n.pluginName,".toggle"),{device:t});case 3:i=o.sent,n.devices[e].on=i.on;case 5:case"end":return o.stop()}}),o)})))()},refresh:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return e.loading=!0,t.prev=1,t.next=4,e.request("".concat(e.pluginName,".switch_status"));case 4:e.devices=t.sent.reduce((function(e,t){var n,o=null!==(n=t.name)&&void 0!==n&&n.length?t.name:t.id;return e[o]=t,e}),{});case 5:return t.prev=5,e.loading=!1,t.finish(5);case 8:case"end":return t.stop()}}),t,null,[[1,,5,8]])})))()}},mounted:function(){var e=this;this.$watch((function(){return e.selected}),(function(t){t&&!e.initialized&&(e.refresh(),e.initialized=!0)})),this.bus.on("refresh",this.onRefreshEvent)},unmounted:function(){this.bus.off("refresh",this.onRefreshEvent)}};t["a"]=c},fe3c:function(e,t,n){"use strict";n("43ec")}}]);
//# sourceMappingURL=chunk-5d632024.e3c77b8b.js.map