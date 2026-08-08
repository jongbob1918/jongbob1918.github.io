export default {
  slug: 'javis', shortName: 'JAVIS', group: 'key',
  title: 'JAVIS — 다목적 모바일 매니퓰레이터',
  description: 'JAVIS ROS 2 시스템 통합과 Navigation 실패 분석 프로젝트',
  team: '9명', period: '2024.09–11',
  skills: ['ROS 2', 'Nav2', 'Smac Planner', 'MPPI', 'System Integration'],
  repository: 'https://github.com/jongbob1918/JAVIS',
  overview: {
    summary: '서로 다른 개발 일정의 주행·로봇팔·AI 모듈을 하나의 임무 흐름으로 연결하고, 협소 공간에서 발생한 주행 실패를 Planner·Controller·Costmap 계층으로 나눠 분석했습니다.'
  },
  demo: { src: '../assets/images/project_javis.png', alt: 'JAVIS 도서관 서비스 로봇', caption: '도서 픽업 임무를 수행하는 JAVIS 시스템. 중앙 제어와 주행 실패 분석에 한정해 설명합니다.' },
  sections: [
    { id: 'pipeline', nav: 'Technical Pipeline', title: 'Technical Pipeline — DMC 임무 흐름', body: `<p>서버 요청을 task executor가 임무 단계로 분해하고, DMC가 drive·arm·AI interface의 완료·실패 응답을 다음 상태 전환 조건으로 사용합니다.</p><div class="diagram" role="img" aria-label="JAVIS 중앙 제어 구조"><div class="diagram-node">사용자 요청<br>Server</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Task Executor<br>Mission</div><div class="diagram-arrow">→</div><div class="diagram-node owner">DMC<br>State &amp; Exception</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Interface<br>Real / Mock</div><div class="diagram-arrow">→</div><div class="diagram-node">Drive · Arm · AI</div></div>` },
    { id: 'technical-details', nav: 'Technical Details', title: 'Technical Details — 인터페이스와 Nav2 판단', body: `<h3>하위 모듈보다 인터페이스를 먼저 고정</h3><p>실장비와 Mock이 동일한 interface를 구현하도록 분리해 하위 모듈 없이도 정상·취소·실패 경로를 반복 실행했습니다.</p><h3>Navigation 실패를 계층 문제로 분해</h3><p>Planner·Controller·Costmap·sensor filtering을 각각 확인하고 Smac Planner Hybrid와 MPPI를 적용했습니다.</p>` },
    { id: 'system', nav: 'System', title: 'System — 중앙 제어와 통합 경계', body: `<div class="role-grid"><div class="info-card"><strong>중앙 제어</strong><span>임무 상태, task executor, 배터리 예외 흐름</span></div><div class="info-card"><strong>Interface &amp; Mock</strong><span>실장비와 모의 응답이 같은 계약을 사용하도록 분리</span></div><div class="info-card"><strong>Navigation</strong><span>Planner·Controller·Costmap 설정 비교 및 조정</span></div></div>` },
    { id: 'hardware', nav: 'Hardware', title: 'Hardware — 이동 베이스와 하위 모듈', body: `<p>시스템은 이동 베이스, 로봇팔, AI 모듈과 배터리 상태 입력으로 구성됩니다. 중앙 제어는 특정 장비 구현에 직접 결합하지 않고 동일한 interface를 통해 실제 장비와 Mock을 교체합니다. 공개 자료에 확인되지 않은 센서·모터 모델과 연산 장치 사양은 기재하지 않습니다.</p>` },
    { id: 'troubleshooting', nav: 'Troubleshooting', title: 'Troubleshooting — 협로 주행 실패', body: `<dl class="flow"><dt>증상</dt><dd>좁은 서가에서 경로가 생성되지 않거나 진입 후 Recovery 과정에서 장애물과 접촉했습니다.</dd><dt>원인</dt><dd>비원형 footprint 표현, 협로 trajectory 탐색, sensor filtering과 inflation 설정이 함께 영향을 줬습니다.</dd><dt>해결</dt><dd>Planner와 Controller를 교체하고 footprint·sensor filter·inflation 관련 값을 함께 조정했습니다.</dd><dt>검증</dt><dd>폭 60cm 테스트 통로를 통과하는 단일 시연을 완료했습니다.</dd></dl>` },
    { id: 'evidence', nav: 'Evidence', title: 'Evidence — 확인된 근거', body: `<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>Interface와 Mock 테스트</strong><p>하위 모듈의 정상·실패 응답을 unittest로 검증합니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>배터리 예외 테스트</strong><p>충전·소모·critical callback과 경계값을 확인합니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>60cm 협로 통과</strong><p>영상으로 확인되는 단일 시연이며 반복 성공률은 아닙니다.</p></div></div>` },
    { id: 'repository', nav: 'Repository', title: 'Repository — 코드와 재현', body: `<p><a class="repo-link" href="https://github.com/jongbob1918/JAVIS/tree/main/javis_ros2/src/javis_dmc" target="_blank" rel="noreferrer">DMC 구현과 테스트 보기 ↗</a></p><p>저장소에는 DMC launch, interface/Mock 단위 테스트와 검증 체크리스트가 있습니다.</p>` }
  ]
};
