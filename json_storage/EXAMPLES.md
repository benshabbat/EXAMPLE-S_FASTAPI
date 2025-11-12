# דוגמאות JSON - קלט לבדיקה

## יצירת משתמשים

```json
{
  "name": "משה כהן",
  "email": "moshe@example.com",
  "age": 25
}
```

```json
{
  "name": "שרה לוי",
  "email": "sara@example.com",
  "age": 32
}
```

```json
{
  "name": "David Smith",
  "email": "david@example.com",
  "age": 28
}
```

## יצירת הערות

```json
{
  "title": "רשימת קניות",
  "content": "חלב, לחם, ביצים, גבינה",
  "tags": ["בית", "קניות"]
}
```

```json
{
  "title": "Meeting Notes",
  "content": "Discussed Q4 goals and deadlines",
  "tags": ["work", "meetings", "important"]
}
```

```json
{
  "title": "רעיונות לפרויקט",
  "content": "1. הוסיף אימות משתמשים\n2. שפר ביצועים\n3. הוסף בדיקות",
  "tags": ["פיתוח", "תכנון"]
}
```

## עדכון חלקי (PATCH)

```json
{
  "title": "כותרת מעודכנת"
}
```

```json
{
  "content": "תוכן חדש לגמרי"
}
```

```json
{
  "tags": ["חדש", "מעודכן"]
}
```

## ייבוא נתונים מלא

```json
{
  "users": [
    {
      "id": 1,
      "name": "Admin User",
      "email": "admin@example.com",
      "age": 35
    },
    {
      "id": 2,
      "name": "Test User",
      "email": "test@example.com",
      "age": 25
    }
  ],
  "notes": [
    {
      "id": 1,
      "title": "Welcome Note",
      "content": "This is a welcome message",
      "tags": ["welcome"]
    }
  ]
}
```

## דוגמאות עם נתונים מורכבים

### משתמש עם פרטים נוספים
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "address": {
    "street": "123 Main St",
    "city": "Tel Aviv",
    "country": "Israel"
  },
  "hobbies": ["reading", "coding", "gaming"]
}
```

### הערה עם מטא-דאטה
```json
{
  "title": "Project Planning",
  "content": "Phase 1: Research\nPhase 2: Development\nPhase 3: Testing",
  "tags": ["project", "planning", "2025"],
  "priority": "high",
  "metadata": {
    "author": "Admin",
    "department": "Engineering",
    "version": "1.0"
  }
}
```
