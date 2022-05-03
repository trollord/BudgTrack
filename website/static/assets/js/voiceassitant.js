const startBtn = document.createElement("button");
startBtn.innerHTML = "Start Listening";
const result = document.createElement("div");
const processing = document.createElement("p");
document.body.append(startBtn);
document.body.append(result);
document.body.append(processing);

// speech to text
window.SpeechRecog = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
let toggleBtn = null;
if (typeof window.SpeechRecog === "undefined") {
    startBtn.remove();
    result.innerHTML = "<b>Browser does not support Speech API. Please download latest chrome.<b>";
} else {
    const recognition = new window.SpeechRecog();
    recognition.continuous = true;
    
    recognition.onresult = event => {
        const last = event.results.length - 1;
        const res = event.results[last];
        const text = res[0].transcript.trim();
        if (res.isFinal) {
            processing.innerHTML = "processing ....";
            
            const response = process(text);
            const p = document.createElement("p");
            p.innerHTML = `You said: ${text} </br>Siri said: ${response}`;
            processing.innerHTML = "";
            result.appendChild(p);

            // read it out
            speechSynthesis.speak(new SpeechSynthesisUtterance(response));
        } else {
            processing.innerHTML = `listening: ${text}`;
        }
    }
    let listening = false;
    toggleBtn = () => {
        if (listening) {
            recognition.stop();
            startBtn.textContent = "Start Listening";
        } else {
            recognition.start();
            startBtn.textContent = "Stop Listening";
        }
        listening = !listening;
    };
    startBtn.addEventListener("click", toggleBtn);

}

// processor
function process(rawText) {
    const q = document.createElement("p");
    let text = rawText.replace(/\s/g, "");
    text = text.toLowerCase();
    let response = null;
    if(!text || text.length === 0 ){
        response = "No voice commmand detected";
    }
    
    if(text.includes("hello")){
        response = "hi, how are you doing?";
    }

    if(text.includes("user")){
        response = `${rawText}`.split("is").pop();
    }

    if(text.includes("name")){
        response = `${rawText}`.split("is").pop();
    }

    else if(text.includes("password")){
        response = `${rawText}`.split("is").pop();
    }

    else if(text.includes("email")){
        response = `${rawText}`.split("is").pop();
    }

    else if(text.includes("howareyou")){
        response = "I'm good.";
    }

    else if(text.includes("whatdowedo")){
        response = "At budgtrack, we can help you manage your money.       You can add, subtract, show your balance or even get your expense report.       It will help you view and study your overall spend analysis using your purchase history";
    }

    else if(text.includes("whomadethis")){
        response = "BudgTrack was developed by Nidhi Kashyap,  Jyotika Kakar, Mandar K and Heer Kapadia";
    }

    else if(text.includes("fine")){
        response = "good.";
    }

    else if(text.includes("login")){
        href = "http://localhost:3000/login";
    }

    else if(text.includes("weather")){
        response = "The weather is humid";
    }
    
    else if(text.includes("thanks") || text.includes("thankyou")){
    	response = "Your Welcome!";
    }

    else if(text.includes("nice")){
    	response = "Thanks!";
    }

    else if(text.includes("time")){
	let hrs = new Date().getHours();
        let am = " PM";
        if(hrs>12){
            hrs = hrs-12;
        }
        else if(hrs==12) am = " PM";
        else am = " AM";
        response = "It's " + hrs + ":" + new Date().getMinutes() + am;
    }

    else if(text.includes("play")){
	let query = rawText.replace("Play","");
	query = query.replace("play","");
        window.open(`https://www.youtube.com/results?search_query=${query}`, "_blank");
        response = "playing" + query;
    }

    else if(text.includes("stop") || text.includes("exit") || text.includes("bye")){
        response = "Bye!";
        toggleBtn();
    }

    if (!response) {
        window.open(`http://google.com/search?q=${rawText.replace("Search", "")}`, "_blank");
        return `I found some information for ${rawText}`;
    }

   if(!text || text.length === 0 ){
        response = "No voice commmand detected";
    }

    return response;
}