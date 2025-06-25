> **Disclaimer**  
> I'm more accustomed to working with Django and Vue/Nuxt. React and FastAPI are relatively new to me, so while tackling this quiz I had to learn them on the fly. Some conventions or best practices might therefore not be strictly followed.

# 🚗 quiz-mercedes-benz

This is a technical challenge from Mercedes Benz.

---

## 🚀 First Time Setup

Before running the application, set up your environment variables for **API** and **Front**:

1. **Navigate** to the `compose` folder
2. **Copy** the example environment file:
   ```bash
   cp .env.example .env
   ```
3. **Edit** the `.env` file with your specific configuration values

---

## 🛠️ Available Commands

### ▶️ To Run

```bash
make clean && make up
```

> **Warning:**  
> `make clean` runs `down -v --remove-orphans`, so it removes all unused volumes.

---

### ⬆️ Up

```bash
make up
```

---

### 🧪 Run Tests

```bash
make test
```

---

### 🧹 Clean Up Everything

_Removes containers, volumes, images:_

```bash
make clean
```

---

### 🔄 Recreate Services

_Down + Up:_

```bash
make recreate
```

---

### 🐚 Access Container Shells

- API container:
  ```bash
  make api-shell
  ```
- Frontend container:
  ```bash
  make front-shell
  ```

---
