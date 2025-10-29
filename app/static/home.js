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

// 초기 로드
loadUser();
