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

    // 페이지네이션 버튼 생성
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    if (page > 1) {
      const prevBtn = document.createElement("button");
      prevBtn.textContent = "이전";
      prevBtn.onclick = () => loadDiaries(page - 1);
      pagination.appendChild(prevBtn);
    }

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
