var nextpage;
var getdata =false;

//網頁一載入
window.onload = function ()
{
    loadimage("",0);
    let index="index";
    checkuser(index);
}



//關鍵字查詢
function clickpic()
{
    let search=document.getElementById("searchtxt").value;
    let input = document.getElementById("div1");
    let input2 = document.getElementById("noinfo");
    input.innerHTML = "";
    input2.innerHTML = "";
    document.getElementById("div1").style.visibility="visible";
    loadimage(search,0);
}


// 載入圖片
function loadimage(key,page)
 {   
                getdata =true;
                let req = new XMLHttpRequest();
                if(page==""){page=0;}
                req.open("GET","/api/attractions?page="+page+"&keyword="+key)
                req.setRequestHeader('Content-type', 'application/json');
                req.onload = function () 
                {
                    let back = JSON.parse(this.response);
                    if (Object.keys(back)[0] != "error")
                    {         
                        var newdata = back["data"];
                        nextpage= back["nextpage"];
                        let count=newdata.length;
                            let stitle ;
                            let pic;
                            let newpic;
                            for (let i=0;i<count;i++)
                            {
                                let ID =  newdata[i]["id"]; 
                                let name = newdata[i]["name"]; 
                                let mrt = newdata[i]["mrt"];
                                if(mrt == null)
                                {
                                    mrt = "";
                                }
                                let category = newdata[i]["category"];
                                let pic = newdata[i]["images"][0].split(',');
                                let newpic = pic[0];
                                let firstdiv = document.getElementById("div1"); //大框架
                                let everydiv = document.createElement("div"); //每個div
                                everydiv.className = "profile" //每個圖片的class
                                firstdiv.appendChild(everydiv); //大框架下每個div

                                let image = document.createElement("img");
                                let br = document.createElement("br");
                                let div_txt = document.createElement("div"); //文字區的div
                                let div_locate = document.createElement("div"); //文字區第一行文字-地點的div
                                let div_MRT = document.createElement("div"); //文字區第一行文字-MRT的div
                                let div_cate = document.createElement("div"); //文字區第一行文字-類別的div
                                let locatename = document.createTextNode(name); //加上文字-地點
                                let locatemrt = document.createTextNode(mrt); //加上文字-捷運
                                let cat = document.createTextNode(category); //加上文字-類別
                                let pic_a = document.createElement("a"); //加上圖片超聯結
                                let a_href = "/attraction/"+ ID  //超連結網址
                                pic_a.setAttribute("href",a_href);
                                everydiv.appendChild(pic_a);
                                image.setAttribute("src",newpic);//插入圖片
                                pic_a.appendChild(image);
                            
                             //  everydiv.appendChild(image); //每個div下的圖片
                                everydiv.appendChild(br); //換行
                            
                                everydiv.appendChild(div_txt);//增加文字的區塊

                                div_txt.appendChild(div_locate)//文字區塊下的第一行-地點
                                div_txt.appendChild(div_MRT)//文字區塊下的第一行-MRT
                                div_txt.appendChild(div_cate)//文字區塊下的第一行-類別

                                div_locate.appendChild(locatename);//加入地點文字

                                div_MRT.appendChild(locatemrt);//加入MRT文字
                                div_cate.appendChild(cat);//加入類別文字

                                div_locate.className = "clasLocate";//地點的CSS
                                div_MRT.className = "classMRT";//MRT的CSS
                                div_cate.className = "classCate";//類別的CSS
                                getdata =false;
                            }
                    }
                    else
                    {
                        document.getElementById("div1").style.visibility="hidden"; 
                        document.getElementById("noinfo").style.visibility="visible"; 
                        let input2 = document.getElementById("noinfo");
                        input2.innerHTML = "查無資料";
                        getdata =false;
                    }
                
                }
                req.send();
        
    }

// 偵測滾輪事件
window.addEventListener("scroll", ()=> {
    const { scrollHeight, clientHeight } = document.documentElement;
    let key = document.getElementById("searchtxt").value;
    if(clientHeight + window.scrollY >= scrollHeight-5)
    {
            if(nextpage != null && getdata == false)
            {
            loadimage(key,nextpage)
            }
    }
});





