# debug_routes.py
import sys
from pathlib import Path

# 🔑 Гарантируем, что корень проекта в пути
sys.path.insert(0, str(Path(__file__).parent))

from main import app

print("\n🔍 === ВСЕ ЗАРЕГИСТРИРОВАННЫЕ РОУТЫ ===")
found_notes = False

for route in app.routes:
    # Пропускаем служебные роуты (static, docs)
    if not hasattr(route, "methods") or not hasattr(route, "path"):
        continue
    
    path = route.path
    methods = sorted(route.methods - {"HEAD", "OPTIONS"})  # убираем автоматические методы
    
    # Ищем наши роуты
    if "notes" in path.lower():
        print(f"  📌 {methods} {path}")
        found_notes = True
    elif "auth" in path.lower() or path in ["/health", "/openapi.json"]:
        print(f"  ✅ {methods} {path}")

print("\n🔍 === ИТОГ ===")
if found_notes:
    print("✅ Роуты /notes НАЙДЕНЫ в приложении!")
    print("❌ Проблема в тестах (скорее всего, base_url или путь)")
else:
    print("❌ Роуты /notes ОТСУТСТВУЮТ в приложении!")
    print("🔧 Проблема в main.py / router.py / импортах")
print("===============================\n")