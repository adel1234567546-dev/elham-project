async function getWisdom() {
    const userInput = document.getElementById('userInput').value;
    const wisdomText = document.getElementById('wisdomText');
    const submitBtn = document.getElementById('submitBtn');

    // 1. التحقق من الإدخال
    if (!userInput.trim()) {
        alert("لطفاً، اكتب ما يقلقك أولاً ليجيبك الحكيم!");
        return;
    }

    // 2. إظهار حالة التحميل وتعطيل الزر
    wisdomText.innerText = 'انتظر يا الذيب ثواني...';
    submitBtn.disabled = true;

    try {
        // 3. الاتصال بالباك إند (FastAPI)
        // ملاحظة: تأكد أن الرابط يطابق الذي يظهر في Terminal (127.0.0.1:8000)
       // غير هذا السطر
const response = await fetch('https://elham-project.onrender.com/get-wisdom', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ problem: userInput })
        });

        const data = await response.json();

        if (response.ok) {
            // 4. تشغيل تأثير الكتابة عند نجاح الرد
            typeWriter(data.wisdom, "wisdomText");
        } else {
            wisdomText.innerText = "عذراً، يبدو أن الحكيم مشغول الآن. حاول لاحقاً.";
        }

    } catch (error) {
        console.error("Error:", error);
        wisdomText.innerText = "حدث خطأ في الاتصال بالسيرفر.";
    } finally {
        // 5. إعادة تفعيل الزر
        submitBtn.disabled = false;
    }
}

// دالة تأثير الكتابة حرفاً بحرف
function typeWriter(text, elementId, speed = 50) {
    const element = document.getElementById(elementId);
    element.innerHTML = ""; // مسح النص الحالي
    let i = 0;

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed); // التحكم في سرعة الكتابة (50 ملي ثانية)
        }
    }
    type();
}
