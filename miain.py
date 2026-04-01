import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# تفعيل اتصال المتصفح (CORS) لضمان عمل الموقع عند النشر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# قراءة المفتاح من بيئة التشغيل (الأمان أولاً)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class ProblemRequest(BaseModel):
    problem: str

@app.post("/get-wisdom")
async def get_wisdom(request: ProblemRequest):
    # التأكد من أن المفتاح موجود قبل محاولة الاتصال بـ Gemini
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="خطأ في الإعدادات: مفتاح الـ API غير متوفر في بيئة التشغيل."
        )

    try:
        # البحث عن أفضل موديل متاح في حسابك
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            raise Exception("لا توجد موديلات متاحة حالياً.")
            
        selected_model = available_models[0]
        model = genai.GenerativeModel(selected_model)
        
        # --- البرومبت الجاهز والفخم ---
        prompt = (
            f"أنت فيلسوف وحكيم عربي قديم، تتحدث بلغة عربية فصحى بليغة وجذابة. "
            f"قدم حكمة أو نصيحة ملهمة وعميقة جداً لمشكلة المستخدم التالية: '{request.problem}'. "
            f"الشروط الصارمة: "
            f"1. الرد يجب أن يكون سطرين واحد فقط لا غير. "
            f"2. لا تذكر مقدمات مثل 'يا بني' أو 'أهلاً بك'. "
            f"3. اجعل العبارة قوية ومؤثرة وكأنها اقتباس تاريخي."
            f"3.حاول تخليها لها صله بل مكتوب."
            f"3.حاول تخدم اشهر المقولات او الحكم."
        )
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return {"wisdom": response.text.strip()}
        else:
            return {"wisdom": "في صمتك تكمن الحكمة التي تبحث عنها."}

    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail="حدث خطأ أثناء استحضار الحكمة.")