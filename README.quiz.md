# Full-Stack Developer Quiz

Thank you very much for filling out this quiz to the best of your competencies. The purpose of this quiz is to evaluate your areas of expertise.

_If a question is not clear to you or uses notations with which you are not familiar, feel free to rephrase the question or lay out assumptions that help you solve the problem._

Good luck and thank you again for your time!

---

# Star Wars Web Application

**Goal:** Build a full‑stack web application that displays and manages data from the Star Wars API (`https://swapi.info/`). The system must be split into two microservices: a backend and a frontend.

**AS A** Star Wars fan

**I WANT** to explore data about People and Planets using a responsive interface,

**SO THAT** I can sort, search, and simulate insights about this information.

## Acceptance Criteria

- [x] 1. **Data Display**

  - [x] Web application reads and displays information from SWAPI (`https://swapi.co/`) in a web browser.
  - [x] Two separate tables: **People** and **Planets**.

- [x] 2. **Pagination**

  - [x] Each table is paginated, displaying **15 items per page**.

- [x] 3. **Search**

  - [x] A search input for filtering by name in each table.
  - [x] Case‑insensitive partial matches (e.g., searching for "sky" in **People** should return "Luke Skywalker").

- [x] 4. **Sorting**

  - [x] Allow sorting by **name** and **created** fields, in both ascending and descending order.
  - [x] Sorting mechanism designed following the _Open‑Closed Principle_ and implemented in the **backend**.

- [x] 5. **Technology Stack**

  - [x] **Frontend:** React (preferred), Angular, or Vue.
  - [x] **Backend:** Python using FastAPI or Flask.

- [x] 6. **Containerization**

  - [x] Use **Docker** to containerize both backend and frontend.
  - [x] Provide a **Docker Compose** setup that runs the system on port **6969**.

---

## Bonus (Optional)

> _These requirements are not mandatory. Not implementing them will not discard you from the hiring process nor reduce points. If implemented, they must work as expected; otherwise, non-working features will not be considered._

- [x] Add a mock endpoint `/simulate-ai-insight` that, given a person or planet name, returns a generated description (fake AI output).
- [x] Add basic logging and/or monitoring to the backend (e.g., log search/sort events).
- [x] Use environment variables to prepare the system for deployment on Azure, AWS, or GCP.
- [x] Add a basic frontend loading state and error display.

---

## Definition of Done

- [x] The application works as defined in the **Acceptance Criteria**.
- [ ] Source code of the web application provided.
- [ ] A clear **README** file explaining how to run the application from scratch using Docker Compose.
- [ ] All integration tests are green.

---

## Evaluation Criteria

- [ ] Adherence to software engineering principles.
- [ ] Quality of UX/UI design.
- [ ] API performance.
- [ ] Clean, maintainable code.

---

_May the Force be with you!_
