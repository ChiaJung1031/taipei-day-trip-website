window.onload=function()
{
   checkuser();
}	

let p_image;
let p_name;
let p_time;
let p_price;
let p_address;
let p_id;
let p_date;
    
    //預定的資訊
function bookinginfo(){
    let request = new XMLHttpRequest();
    request.open("GET","/api/booking")
    request.onload = function()
        {
            let data = JSON.parse(this.response);
            console.log(data["data"])
            if(data["data"] != null)
            {   
                p_id = data["data"]["attraction"]["id"];
                let pic = document.getElementById("picture");
                pic.setAttribute("src",data["data"]["attraction"]["image"]);//插入圖片
                p_image=data["data"]["attraction"]["image"];
                let subtitle = document.getElementById("subtitle");
                subtitle.innerHTML="台北一日遊："+data["data"]["attraction"]["name"];
                p_name=data["data"]["attraction"]["name"];
                let date = document.getElementById("date");
                date.innerHTML= data["data"]["date"];
                p_date=data["data"]["date"];
                let time = document.getElementById("time");
                if(data["data"]["time"] == "morning")
                {
                    p_time= data["data"]["time"];
                    time.innerHTML= "早上 9 點到下午 4 點";
                }
                else
                {
                    p_time= data["data"]["time"];
                    time.innerHTML= "下午 2 點到晚上 9 點";
                }
                let price = document.getElementById("price");
                price.innerHTML= "新台幣"+ data["data"]["price"]+"元";
                p_price =data["data"]["price"];
                let address = document.getElementById("address");
                address.innerHTML=data["data"]["attraction"]["address"];
                p_address=data["data"]["attraction"]["address"];
                let totalprice = document.getElementById("totalprice");
                totalprice.innerHTML="總價：新台幣"+data["data"]["price"]+"元";
            }
            else
            {
                let nobooking=document.getElementById("nobooking");
                let isbooking=document.getElementById("isbooking");
                let footer=document.getElementById("footer");
                footer.style.height="100%";
                nobooking.innerHTML="目前沒有任何待預訂的行程";
                nobooking.style.display="block";
                isbooking.style.display="none";
            }
    
        }
        request.send();
    }
    
    //刪除預定行程
function deletebook()
{
        let req = new XMLHttpRequest();
        req.open("DELETE","/api/booking")
        req.onload = function () 
            {
                let data = JSON.parse(this.response);
                if(Object.keys(data)[0] == "ok")
                {
                    self.location="/";
                }
                else
                {
                    let error = data["message"];
                    alert(error);
                }
            }
            req.send();
    
}
    
    
    
    //信用卡號輸入自動空格
function keyup(obj){
        var v = obj.value;
        console.info(v);
        v =v.replace(/(\s)/g,'').replace(/(\d{4})/g,'$1 ').replace(/\s*$/,'')
        obj.value =v;
    }
    
    
    
//金流串接
//TPDirect.setupSDK 設定參數
TPDirect.setupSDK(20410, 'app_6kKSn4u2u1s6pgS7hXRxMaLLhygWHuSSazLpsGAlPM5GX9mlKCEjTapkC4H6', 'sandbox')


