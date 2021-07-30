window.onload = function ()
{
   let index="index";
   checkuser(index);

   var count;

   //rbt預設上午場
   if(document.getElementById('date_m').checked == true)
   {
       radio_value = document.getElementById('radio_value');
       let cat = document.createTextNode("新台幣2000元"); 
       radio_value.appendChild(cat);  
   }

   //產內容
   let req = new XMLHttpRequest();
   console.log(location.pathname)
   req.open("GET","/api"+location.pathname)
   req.setRequestHeader('Content-type', 'application/json');
   req.onload = function () 
   {
       let back = JSON.parse(this.response);
        console.log(back["data"][0])
        let name = back["data"][0]["name"];
        let category = back["data"][0]["category"];
        let MRT = back["data"][0]["mrt"]; 
        let description = back["data"][0]["description"];
        let add = back["data"][0]["address"];
        let trans = back["data"][0]["transport"];  
        if(MRT== null)
        {
           let catMRT =  category + " " + "at" +  " " + "" ;
           let subtitle = document.getElementById("subtitle") ;
           subtitle.innerHTML=catMRT;
        }
        else
        {
           let catMRT =  category + " " + "at" +  " " + MRT ;
           let subtitle = document.getElementById("subtitle") ;
           subtitle.innerHTML=catMRT;
        }
        let title = document.getElementById("title") ;
        title.innerHTML=name;
        let introduce = document.getElementById("introduce") ;
        introduce.innerHTML=description;
        let address = document.getElementById("address") ;
        address.innerHTML=add;
        let transport = document.getElementById("transport") ;
        transport.innerHTML=trans;

        let pic =  back["data"][0]["images"];
        console.log(pic)
        count =pic.split(',').length; //圖片數量
        let picList = document.getElementById("list"); //圖片div
        let PicLast = document.createElement("img");//產生最後一張圖片
        PicLast.setAttribute("src",pic.split(',')[(count-1)]);//插入圖片
        picList.appendChild(PicLast);
        for(i=0;i<count;i++)
        {
           let allPic = document.createElement("img");//產生所有圖片
           allPic.setAttribute("src",pic.split(',')[i]);//插入圖片
           picList.appendChild(allPic);
        }
        let PicFirst = document.createElement("img");//產生第一張圖片
        PicFirst.setAttribute("src",pic.split(',')[0]);//插入圖片
        picList.appendChild(PicFirst);
   }
    req.send();



    
//輪播
var container = document.getElementById('container');
var list = document.getElementById('list');
var prev = document.getElementById('prev');
var next = document.getElementById('next');
var timer;
function animate(offset) {
       var newLeft = parseInt(list.style.left) + offset;
       list.style.left = newLeft + 'px';
       //一直滾動
       if (newLeft > -600) {
           list.style.left = -600 * (count) + 'px';
       }
       if (newLeft < -600 * (count)) {
           list.style.left = -600 + 'px';
       }
   }

   prev.onclick = function () {
       animate(600);
   };

   next.onclick = function () {
       animate(-600);
   
   };
}

//click radio btn
function radioClick(radioValue)
{
   if (radioValue.value == "morning")
   {
       radio_value = document.getElementById('radio_value');
       radio_value.innerHTML = "";
       let cat = document.createTextNode("新台幣2000元"); 
       radio_value.appendChild(cat); 
   }
   else if (radioValue.value == "afternoon")
   {
       radio_value = document.getElementById('radio_value');
       radio_value.innerHTML = "";
       let cat = document.createTextNode("新台幣2500元"); 
       radio_value.appendChild(cat);  
   }

}



//開始預訂
function startbook()
{
   let id = location.pathname.split('/')[2];
   let date = document.getElementById("datetime").value;
   let time = document.getElementsByName("demo-radio");
   let timeval="";
   let price ="";

   if(time[0].checked)
   {
       timeval=time[0].value;
       price = "2000";
   }
   else if(time[1].checked)
   {
       timeval=time[1].value;
       price = "2500";
   }
   
   if(date == "") //判斷日期未填
   {
       alert("請選擇日期")
   }
   else if(Date.parse(date) < Date.parse((new Date()).toDateString()))
   {
       alert("日期不可小於今日")
   }
   else
   {
       let startbook="startbook";
       checkuser(startbook);  //確認是否有登入才能進行預定
       let booking = {attractionId:id,date:date,time:timeval,price:price}
       let data = JSON.stringify(booking);
       let req = new XMLHttpRequest();
       req.open("POST","/api/booking")
       req.setRequestHeader('Content-type', 'application/json');
       req.send(data);
       req.onload = function(){
           let response= JSON.parse(this.response);
           if(Object.keys(response)[0] == "ok")
           {
               self.location="/booking";
           }
           else
           {
               let error = response["message"];
               alert(error);
           }
       };

   }
 
}

