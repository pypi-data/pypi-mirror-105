(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-5c4852cd"],{"10ff":function(e,t,n){"use strict";n.r(t);n("b0c0"),n("b64b");var r=n("7a23"),c={class:"row plugin execute-container"},a={class:"command-container"},s=Object(r["h"])("div",{class:"title"},"Execute Action",-1),o={class:"request-type-container"},i=Object(r["h"])("label",{for:"action-structured-input"},"Structured request",-1),l=Object(r["h"])("label",{for:"action-raw-input"},"Raw request",-1),u={class:"autocomplete"},d=Object(r["h"])("i",{class:"fas fa-play"},null,-1),b={key:0,class:"doc-container"},h=Object(r["h"])("div",{class:"title"}," Action documentation ",-1),p={key:1,class:"options"},O={key:0,class:"params",ref:"params"},j={key:0,class:"attr-doc-container mobile"},f={class:"title"},m=Object(r["g"])(" Attribute: "),v={key:0,class:"extra-params",ref:"extraParams"},g={class:"col-5"},y={class:"col-5"},x={class:"col-2 buttons"},k=Object(r["h"])("i",{class:"fas fa-trash"},null,-1),A={key:1,class:"add-param"},C=Object(r["h"])("i",{class:"fas fa-plus"},null,-1),D={key:1,class:"attr-doc-container widescreen"},w={class:"title"},P=Object(r["g"])(" Attribute: "),E={class:"output-container"},L={class:"first-row"},T=Object(r["h"])("i",{class:"fas fa-play"},null,-1),N={key:0,class:"output-container"},I={class:"procedures-container"},S=Object(r["h"])("div",{class:"title"},"Execute Procedure",-1),q={class:"head"},M={class:"btn-container col-no-margin-1"},H=Object(r["h"])("i",{class:"fas fa-play"},null,-1),R={key:0,class:"params"};function J(e,t,n,J,V,U){var F=Object(r["z"])("Loading");return Object(r["r"])(),Object(r["e"])("div",c,[V.loading?(Object(r["r"])(),Object(r["e"])(F,{key:0})):Object(r["f"])("",!0),Object(r["h"])("div",a,[s,Object(r["h"])("form",{class:"action-form",ref:"actionForm",autocomplete:"off",onSubmit:t[9]||(t[9]=Object(r["J"])((function(){return U.executeAction&&U.executeAction.apply(U,arguments)}),["prevent"]))},[Object(r["h"])("div",o,[Object(r["h"])("input",{type:"radio",id:"action-structured-input",checked:V.structuredInput,onChange:t[1]||(t[1]=function(e){return U.onInputTypeChange(!0)})},null,40,["checked"]),i,Object(r["h"])("input",{type:"radio",id:"action-raw-input",checked:!V.structuredInput,onChange:t[2]||(t[2]=function(e){return U.onInputTypeChange(!1)})},null,40,["checked"]),l]),Object(r["h"])("div",{class:["request structured-request",V.structuredInput?"":"hidden"]},[Object(r["h"])("div",u,[Object(r["h"])("label",null,[Object(r["I"])(Object(r["h"])("input",{ref:"actionName",type:"text",class:"action-name",placeholder:"Action Name",disabled:V.running,"onUpdate:modelValue":t[3]||(t[3]=function(e){return V.action.name=e}),onChange:t[4]||(t[4]=function(e){return V.actionChanged=!0}),onBlur:t[5]||(t[5]=function(){return U.updateAction&&U.updateAction.apply(U,arguments)})},null,40,["disabled"]),[[r["F"],V.action.name]])])]),Object(r["h"])("button",{type:"submit",class:"run-btn btn-primary",disabled:V.running,title:"Run"},[d],8,["disabled"]),V.selectedDoc?(Object(r["r"])(),Object(r["e"])("div",b,[h,V.htmlDoc?(Object(r["r"])(),Object(r["e"])("div",{key:0,class:"doc html",innerHTML:V.selectedDoc},null,8,["innerHTML"])):(Object(r["r"])(),Object(r["e"])("div",{key:1,class:"doc raw",textContent:Object(r["C"])(V.selectedDoc)},null,8,["textContent"]))])):Object(r["f"])("",!0),V.action.name in V.actions&&(Object.keys(V.action.args).length||V.action.supportsExtraArgs)?(Object(r["r"])(),Object(r["e"])("div",p,[Object.keys(V.action.args).length||V.action.supportsExtraArgs?(Object(r["r"])(),Object(r["e"])("div",O,[(Object(r["r"])(!0),Object(r["e"])(r["a"],null,Object(r["x"])(Object.keys(V.action.args),(function(e){return Object(r["r"])(),Object(r["e"])("div",{class:"param",key:e},[Object(r["h"])("label",null,[Object(r["I"])(Object(r["h"])("input",{type:"text",class:"action-param-value",disabled:V.running,placeholder:e,"onUpdate:modelValue":function(t){return V.action.args[e].value=t},onFocus:function(t){return U.selectAttrDoc(e)},onBlur:t[6]||(t[6]=function(){return U.resetAttrDoc&&U.resetAttrDoc.apply(U,arguments)})},null,40,["disabled","placeholder","onUpdate:modelValue","onFocus"]),[[r["F"],V.action.args[e].value]])]),V.selectedAttrDoc&&V.selectedAttr===e?(Object(r["r"])(),Object(r["e"])("div",j,[Object(r["h"])("div",f,[m,Object(r["h"])("div",{class:"attr-name",textContent:Object(r["C"])(V.selectedAttr)},null,8,["textContent"])]),V.htmlDoc?(Object(r["r"])(),Object(r["e"])("div",{key:0,class:"doc html",innerHTML:V.selectedAttrDoc},null,8,["innerHTML"])):(Object(r["r"])(),Object(r["e"])("div",{key:1,class:"doc raw",textContent:Object(r["C"])(V.selectedAttrDoc)},null,8,["textContent"]))])):Object(r["f"])("",!0)])})),128)),Object.keys(V.action.extraArgs).length?(Object(r["r"])(),Object(r["e"])("div",v,[(Object(r["r"])(!0),Object(r["e"])(r["a"],null,Object(r["x"])(Object.keys(V.action.extraArgs),(function(e){return Object(r["r"])(),Object(r["e"])("div",{class:"param extra-param",key:e},[Object(r["h"])("label",g,[Object(r["I"])(Object(r["h"])("input",{type:"text",class:"action-extra-param-name",disabled:V.running,placeholder:"Name","onUpdate:modelValue":function(t){return V.action.extraArgs[e].name=t}},null,8,["disabled","onUpdate:modelValue"]),[[r["F"],V.action.extraArgs[e].name]])]),Object(r["h"])("label",y,[Object(r["I"])(Object(r["h"])("input",{type:"text",class:"action-extra-param-value",disabled:V.running,placeholder:"Value","onUpdate:modelValue":function(t){return V.action.extraArgs[e].value=t}},null,8,["disabled","onUpdate:modelValue"]),[[r["F"],V.action.extraArgs[e].value]])]),Object(r["h"])("label",x,[Object(r["h"])("button",{type:"button",class:"action-extra-param-del",title:"Remove parameter",onClick:function(t){return U.removeParameter(e)}},[k],8,["onClick"])])])})),128))],512)):Object(r["f"])("",!0),V.action.supportsExtraArgs?(Object(r["r"])(),Object(r["e"])("div",A,[Object(r["h"])("button",{type:"button",title:"Add a parameter",onClick:t[7]||(t[7]=function(){return U.addParameter&&U.addParameter.apply(U,arguments)})},[C])])):Object(r["f"])("",!0)],512)):Object(r["f"])("",!0),V.selectedAttrDoc?(Object(r["r"])(),Object(r["e"])("div",D,[Object(r["h"])("div",w,[P,Object(r["h"])("div",{class:"attr-name",textContent:Object(r["C"])(V.selectedAttr)},null,8,["textContent"])]),V.htmlDoc?(Object(r["r"])(),Object(r["e"])("div",{key:0,class:"doc html",innerHTML:V.selectedAttrDoc},null,8,["innerHTML"])):(Object(r["r"])(),Object(r["e"])("div",{key:1,class:"doc raw",textContent:Object(r["C"])(V.selectedAttrDoc)},null,8,["textContent"]))])):Object(r["f"])("",!0),Object(r["h"])("div",E,[null!=V.error||null!=V.response?(Object(r["r"])(),Object(r["e"])("div",{key:0,class:"title",textContent:Object(r["C"])(null!=V.error?"Error":"Output")},null,8,["textContent"])):Object(r["f"])("",!0),null!=V.response?(Object(r["r"])(),Object(r["e"])("div",{key:1,class:"response",innerHTML:V.response},null,8,["innerHTML"])):null!=V.error?(Object(r["r"])(),Object(r["e"])("div",{key:2,class:"error",innerHTML:V.error},null,8,["innerHTML"])):Object(r["f"])("",!0)])])):Object(r["f"])("",!0)],2),Object(r["h"])("div",{class:["request raw-request",V.structuredInput?"hidden":""]},[Object(r["h"])("div",L,[Object(r["h"])("label",null,[Object(r["I"])(Object(r["h"])("textarea",{"onUpdate:modelValue":t[8]||(t[8]=function(e){return V.rawRequest=e}),placeholder:"Raw JSON request"},null,512),[[r["F"],V.rawRequest]])]),Object(r["h"])("button",{type:"submit",disabled:V.running,class:"run-btn btn-primary",title:"Run"},[T],8,["disabled"])]),null!=V.response||null!=V.error?(Object(r["r"])(),Object(r["e"])("div",N,[Object(r["h"])("div",{class:"title",textContent:Object(r["C"])(null!=V.error?"Error":"Output")},null,8,["textContent"]),null!=V.error?(Object(r["r"])(),Object(r["e"])("div",{key:0,class:"error",innerHTML:V.error},null,8,["innerHTML"])):null!=V.response?(Object(r["r"])(),Object(r["e"])("div",{key:1,class:"response",innerHTML:V.response},null,8,["innerHTML"])):Object(r["f"])("",!0)])):Object(r["f"])("",!0)],2)],544)]),Object(r["h"])("div",I,[S,(Object(r["r"])(!0),Object(r["e"])(r["a"],null,Object(r["x"])(Object.keys(V.procedures).sort(),(function(n){return Object(r["r"])(),Object(r["e"])("div",{class:["procedure",V.selectedProcedure.name===n?"selected":""],key:n,onClick:function(e){return U.updateProcedure(n,e)}},[Object(r["h"])("form",{ref:"procedureForm",autocomplete:"off",onSubmit:t[12]||(t[12]=Object(r["J"])((function(){return U.executeProcedure&&U.executeProcedure.apply(U,arguments)}),["prevent"]))},[Object(r["h"])("div",q,[Object(r["h"])("div",{class:"name col-no-margin-11",textContent:Object(r["C"])(n)},null,8,["textContent"]),Object(r["h"])("div",M,[V.selectedProcedure.name===n?(Object(r["r"])(),Object(r["e"])("button",{key:0,type:"submit",class:"run-btn btn-default",disabled:V.running,title:"Run",onClick:t[10]||(t[10]=Object(r["J"])((function(t){return e.$emit("submit")}),["stop"]))},[H],8,["disabled"])):Object(r["f"])("",!0)])]),V.selectedProcedure.name===n?(Object(r["r"])(),Object(r["e"])("div",R,[(Object(r["r"])(!0),Object(r["e"])(r["a"],null,Object(r["x"])(Object.keys(V.selectedProcedure.args),(function(e){return Object(r["r"])(),Object(r["e"])("div",{class:"param",key:e},[Object(r["h"])("label",null,[Object(r["I"])(Object(r["h"])("input",{type:"text",class:"action-param-value",onClick:t[11]||(t[11]=function(e){return e.stopPropagation()}),disabled:V.running,placeholder:e,"onUpdate:modelValue":function(t){return V.selectedProcedure.args[e]=t}},null,8,["disabled","placeholder","onUpdate:modelValue"]),[[r["F"],V.selectedProcedure.args[e]]])])])})),128))])):Object(r["f"])("",!0)],544)],10,["onClick"])})),128))])])}var V=n("5530"),U=n("1da1");n("96cf"),n("07ac"),n("4fad"),n("ac1f"),n("1276"),n("466d"),n("2ca0"),n("498a"),n("fb6a"),n("d3b7"),n("25f0");function F(e,t,n){var r;function c(e){if(!e)return!1;a(e),r>=e.length&&(r=0),r<0&&(r=e.length-1),e[r].classList.add("autocomplete-active")}function a(e){for(var t=0;t<e.length;t++)e[t].classList.remove("autocomplete-active")}function s(t){for(var n=document.getElementsByClassName("autocomplete-items"),r=0;r<n.length;r++)t!==n[r]&&t!==e&&n[r].parentNode.removeChild(n[r])}e.addEventListener("input",(function(){var c,a,o,i=this.value;if(s(),!i)return!1;for(r=-1,c=document.createElement("DIV"),c.setAttribute("id",this.id+"autocomplete-list"),c.setAttribute("class","autocomplete-items"),this.parentNode.appendChild(c),o=0;o<t.length;o++)t[o].substr(0,i.length).toUpperCase()===i.toUpperCase()&&(a=document.createElement("DIV"),a.innerHTML="<strong>"+t[o].substr(0,i.length)+"</strong>",a.innerHTML+=t[o].substr(i.length),a.innerHTML+="<input type='hidden' value='"+t[o]+"'>",a.addEventListener("click",(function(t){e.value=this.getElementsByTagName("input")[0].value,n&&n(t,e.value),s()})),c.appendChild(a))})),e.addEventListener("keydown",(function(e){9===e.keyCode&&s()})),e.addEventListener("keydown",(function(e){var t=document.getElementById(this.id+"autocomplete-list");t&&(t=t.getElementsByTagName("div")),40===e.keyCode?(r++,c(t)):38===e.keyCode?(r--,c(t)):13===e.keyCode&&r>-1&&t&&t.length&&(e.preventDefault(),t[r].click(),this.focus())})),document.addEventListener("click",(function(e){s(e.target)}))}var _=F,B=n("3e54"),W=n("3a5e"),$={name:"Execute",components:{Loading:W["a"]},mixins:[B["a"]],data:function(){return{loading:!1,running:!1,structuredInput:!0,actionChanged:!1,selectedDoc:void 0,selectedAttr:void 0,selectedAttrDoc:void 0,selectedProcedure:{name:void 0,args:{}},response:void 0,error:void 0,htmlDoc:!1,rawRequest:void 0,actions:{},plugins:{},procedures:{},action:{name:void 0,args:{},extraArgs:[],supportsExtraArgs:!1}}},methods:{refresh:function(){var e=this;return Object(U["a"])(regeneratorRuntime.mark((function t(){var n,r,c,a,s,o,i;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return e.loading=!0,t.prev=1,t.next=4,e.request("inspect.get_procedures");case 4:return e.procedures=t.sent,t.next=7,e.request("inspect.get_all_plugins",{html_doc:!1});case 7:e.plugins=t.sent;case 8:return t.prev=8,e.loading=!1,t.finish(8);case 11:for(n=0,r=Object.values(e.plugins);n<r.length;n++)for(c=r[n],c.html_doc&&(e.htmlDoc=!0),a=0,s=Object.values(c.actions);a<s.length;a++)o=s[a],o.name=c.name+"."+o.name,o.supportsExtraArgs=!!o.has_kwargs,delete o.has_kwargs,e.actions[o.name]=o;i=e,_(e.$refs.actionName,Object.keys(e.actions).sort(),(function(t,n){e.action.name=n,i.updateAction()}));case 14:case"end":return t.stop()}}),t,null,[[1,,8,11]])})))()},updateAction:function(){if(this.action.name in this.actions||(this.selectedDoc=void 0),this.actionChanged&&this.action.name in this.actions){this.loading=!0;try{this.action=Object(V["a"])(Object(V["a"])({},this.actions[this.action.name]),{},{args:Object.entries(this.actions[this.action.name].args).reduce((function(e,t){return e[t[0]]=Object(V["a"])(Object(V["a"])({},t[1]),{},{value:t[1].default}),e}),{}),extraArgs:[]})}finally{this.loading=!1}this.selectedDoc=this.parseDoc(this.action.doc),this.actionChanged=!1,this.response=void 0,this.error=void 0}},parseDoc:function(e){if(null===e||void 0===e||!e.length||this.htmlDoc)return e;var t=0,n=0;return e.split("\n").reduce((function(e,r){return 2===++t&&(n=r.match(/^(\s*)/)[1].length),r.trim().startsWith(".. code-block")||(e+=r.slice(n).replaceAll("``","")+"\n"),e}),"")},updateProcedure:function(e,t){"submit"!==t.target.getAttribute("type")&&(this.selectedProcedure.name!==e?e in this.procedures?this.selectedProcedure={name:e,args:(this.procedures[e].args||[]).reduce((function(e,t){return e[t]=void 0,e}),{})}:console.warn("Procedure not found: "+e):this.selectedProcedure={name:void 0,args:{}})},addParameter:function(){this.action.extraArgs.push({name:void 0,value:void 0})},removeParameter:function(e){this.action.extraArgs.pop(e)},selectAttrDoc:function(e){this.response=void 0,this.error=void 0,this.selectedAttr=e,this.selectedAttrDoc=this.parseDoc(this.action.args[e].doc)},resetAttrDoc:function(){this.response=void 0,this.error=void 0,this.selectedAttr=void 0,this.selectedAttrDoc=void 0},onInputTypeChange:function(e){this.structuredInput=e,this.response=void 0,this.error=void 0},onResponse:function(e){this.response="<pre>"+JSON.stringify(e,null,2)+"</pre>",this.error=void 0},onError:function(e){this.response=void 0,this.error=e},onDone:function(){this.running=!1},executeAction:function(){if((this.action.name||this.rawRequest)&&!this.running)if(this.running=!0,this.structuredInput){var e=Object(V["a"])(Object(V["a"])({},Object.entries(this.action.args).reduce((function(e,t){if(null!=t[1].value){var n=t[1].value;try{n=JSON.parse(n)}catch(r){console.debug("Not a valid JSON value"),console.debug(n)}e[t[0]]=n}return e}),{})),this.action.extraArgs.reduce((function(e,t){var n=e[t.value];try{n=JSON.parse(n)}catch(r){console.debug("Not a valid JSON value"),console.debug(n)}return e[t.name]=n,e}),{}));this.request(this.action.name,e).then(this.onResponse).catch(this.onError).finally(this.onDone)}else try{var t=JSON.parse(this.rawRequest);this.execute(t).then(this.onResponse).catch(this.onError).finally(this.onDone)}catch(n){this.notify({error:!0,title:"Invalid JSON request",text:n.toString()})}},executeProcedure:function(e){if(this.selectedProcedure.name&&!this.running){e.stopPropagation(),this.running=!0;var t=Object(V["a"])({},Object.entries(this.selectedProcedure.args).reduce((function(e,t){if(null!=t[1]){var n=t[1];try{n=JSON.parse(n)}catch(r){console.debug("Not a valid JSON value"),console.debug(n)}e[t[0]]=n}return e}),{}));this.request("procedure."+this.selectedProcedure.name,t).then(this.onResponse).catch(this.onError).finally(this.onDone)}}},mounted:function(){this.refresh()}};n("3d4f");$.render=J;t["default"]=$},"2ca0":function(e,t,n){"use strict";var r=n("23e7"),c=n("06cf").f,a=n("50c4"),s=n("5a34"),o=n("1d80"),i=n("ab13"),l=n("c430"),u="".startsWith,d=Math.min,b=i("startsWith"),h=!l&&!b&&!!function(){var e=c(String.prototype,"startsWith");return e&&!e.writable}();r({target:"String",proto:!0,forced:!h&&!b},{startsWith:function(e){var t=String(o(this));s(e);var n=a(d(arguments.length>1?arguments[1]:void 0,t.length)),r=String(e);return u?u.call(t,r,n):t.slice(n,n+r.length)===r}})},"3d4f":function(e,t,n){"use strict";n("ee13")},"498a":function(e,t,n){"use strict";var r=n("23e7"),c=n("58a8").trim,a=n("c8d2");r({target:"String",proto:!0,forced:a("trim")},{trim:function(){return c(this)}})},"5a34":function(e,t,n){var r=n("44e7");e.exports=function(e){if(r(e))throw TypeError("The method doesn't accept regular expressions");return e}},ab13:function(e,t,n){var r=n("b622"),c=r("match");e.exports=function(e){var t=/./;try{"/./"[e](t)}catch(n){try{return t[c]=!1,"/./"[e](t)}catch(r){}}return!1}},c8d2:function(e,t,n){var r=n("d039"),c=n("5899"),a="​᠎";e.exports=function(e){return r((function(){return!!c[e]()||a[e]()!=a||c[e].name!==e}))}},ee13:function(e,t,n){}}]);
//# sourceMappingURL=chunk-5c4852cd.d9005e74.js.map