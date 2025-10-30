// JWT 토큰 가져오기
const token = localStorage.getItem("token");

// 사용자 정보 불러오기
async function loadUser() {
  const res = await fetch("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.ok) {
    const data = await res.json();
    document.getElementById("username").textContent = data.username;
  } else {
    alert("세션이 만료되었습니다. 다시 로그인해주세요.");
    localStorage.removeItem("token");
    window.location.href = "/";
  }
}

// 로그아웃 버튼 클릭 시
document.getElementById("logout-btn").addEventListener("click", async () => {
  await fetch("/auth/logout", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  localStorage.removeItem("token");
  alert("로그아웃 되었습니다.");
  window.location.href = "/";
});


// 일기 작성
document.getElementById("diary-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = e.target.title.value;
  const content = e.target.content.value;

  const res = await fetch("/diary/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, content }),
  });

  if (res.ok) {
    alert("일기가 저장되었습니다!");
    e.target.reset();
    loadDiaries();
  } else {
    alert("일기 저장 실패");
  }
});

// 일기 목록 불러오기 (페이지네이션 포함)
async function loadDiaries(page = 1) {
  const token = localStorage.getItem("token");

  if (!token) {
    alert("로그인이 필요합니다.");
    window.location.href = "/";
    return;
  }

  const res = await fetch(`/diary/list?page=${page}&limit=5`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  const list = document.getElementById("diary-list");
  list.innerHTML = "";

  if (res.ok) {
    const data = await res.json();

    // 일기 목록 표시
    data.items.forEach((d) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${d.diary_title}</strong><br>
        ${d.diary_content}<br>
        <small>${new Date(d.created_at).toLocaleString()}</small>
      `;
      list.appendChild(li);
    });

    // 페이지네이션 UI 구성
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    // 이전 버튼
    if (page > 1) {
      const prevBtn = document.createElement("button");
      prevBtn.textContent = "이전";
      prevBtn.onclick = () => loadDiaries(page - 1);
      pagination.appendChild(prevBtn);
    }

    // 현재 페이지 표시 👇
    const pageInfo = document.createElement("span");
    pageInfo.textContent = ` ${page} `;
    pageInfo.style.margin = "0 10px";
    pageInfo.style.fontWeight = "bold";
    pagination.appendChild(pageInfo);

    // 다음 버튼
    if (data.has_next) {
      const nextBtn = document.createElement("button");
      nextBtn.textContent = "다음";
      nextBtn.onclick = () => loadDiaries(page + 1);
      pagination.appendChild(nextBtn);
    }
  } else {
    list.innerHTML = "<li>일기를 불러올 수 없습니다.</li>";
  }
}

// 페이지 로드 시 첫 페이지 불러오기
document.addEventListener("DOMContentLoaded", () => loadDiaries(1));


// 초기 로드
loadUser();
