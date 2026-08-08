export default {
  slug: 'roomie', shortName: 'ROOMIE', group: 'key',
  title: 'ROOMIE — 엘리베이터 버튼 조작 로봇',
  description: 'ROOMIE 4-DOF 로봇팔 좌표변환, IK, FreeRTOS 제어 프로젝트',
  team: '4명', period: '2025.07.07–08.13',
  skills: ['ROS 2', '4-DOF Arm', 'Hand-Eye Calibration', 'IK', 'FreeRTOS', 'ESP32'],
  repository: 'https://github.com/jongbob1918/ROOMIE',
  overview: {
    summary: '카메라에서 얻은 버튼 위치를 로봇 기준 좌표와 4개 관절각으로 변환하고, 통신과 모션 갱신을 분리한 ESP32 제어기로 실제 버튼 조작까지 연결했습니다.'
  },
  demo: { src: '../assets/images/elevator-pushouterbutton2.gif', alt: 'ROOMIE 로봇팔의 엘리베이터 버튼 조작' },
  sections: [
    { id: 'pipeline', nav: 'Technical Pipeline', title: 'Technical Pipeline — 인식부터 모터 명령까지', body: `<div class="diagram" role="img" aria-label="ROOMIE 버튼 조작 파이프라인"><div class="diagram-node">Button BBox<br>Vision</div><div class="diagram-arrow">→</div><div class="diagram-node owner">PnP · Hand-Eye<br>3D Target</div><div class="diagram-arrow">→</div><div class="diagram-node owner">IK<br>4 Joint Angles</div><div class="diagram-arrow">→</div><div class="diagram-node owner">Serial Command<br>ESP32</div><div class="diagram-arrow">→</div><div class="diagram-node owner">FreeRTOS<br>4 Servos</div></div><p>관측, 접근, 정렬, 누르기를 분리하고 IK 해가 허용 오차나 관절 범위를 벗어나면 명령을 보내지 않습니다.</p>` },
    { id: 'technical-details', nav: 'Technical Details', title: 'Technical Details — 좌표변환과 모션 프로파일', body: `<h3>카메라 좌표를 로봇 기준으로 변환</h3><p>solvePnPRansac과 Hand-Eye calibration, 현재 관절의 순기구학 결과를 결합합니다.</p><div class="formula-block">T_base→button = T_base→tool · T_tool→camera · T_camera→button</div><h3>IK 해 검증</h3><p>계산한 관절각으로 forward kinematics를 다시 수행하고 위치 오차와 관절 범위를 검사합니다.</p><div class="formula-block">e_IK = ‖p_FK(q*) − p_target‖₂ ≤ 0.001 m</div><h3>Gaussian 모션 보간</h3><p>ESP32의 모션 task는 시작각과 목표각 사이를 Gaussian 누적함수 기반으로 갱신합니다.</p>` },
    { id: 'system', nav: 'System', title: 'System — 제어 책임과 통합 경계', body: `<div class="role-grid"><div class="info-card"><strong>Pose &amp; IK</strong><span>Hand-Eye 좌표변환과 4관절 해 계산</span></div><div class="info-card"><strong>Motion Control</strong><span>ROS 2–serial–ESP32 명령 흐름과 보간</span></div><div class="info-card"><strong>Integration</strong><span>접근·정렬·누르기 시퀀스와 GUI 연동</span></div></div>` },
    { id: 'hardware', nav: 'Hardware', title: 'Hardware — 4-DOF Arm과 ESP32', body: `<p>4개의 서보 모터로 구성된 로봇팔을 ESP32가 구동하고, 카메라 관측값은 ROS 2 제어 노드에서 좌표변환과 IK를 거쳐 관절 명령으로 변환됩니다. encoder나 force sensor 기반 접촉 피드백이 확인되지 않아 명령 기반 open-loop actuator control로 설명합니다.</p>` },
    { id: 'troubleshooting', nav: 'Troubleshooting', title: 'Troubleshooting — 빗맞힘과 진동', body: `<dl class="flow"><dt>증상</dt><dd>정지 순간 팔끝이 흔들리고 계산된 버튼 위치와 실제 접촉점이 어긋났습니다.</dd><dt>원인</dt><dd>좌표계 장착 오차, 급격한 관절각 변화와 blocking serial 처리가 함께 영향을 줬습니다.</dd><dt>해결</dt><dd>Hand-Eye 변환을 적용하고 통신과 모션 task를 서로 다른 core에 배치했으며 Gaussian 보간을 적용했습니다.</dd><dt>검증</dt><dd>버튼 인식부터 실제 누르기까지 연속 동작을 완료했습니다.</dd></dl>` },
    { id: 'evidence', nav: 'Evidence', title: 'Evidence — 확인된 근거', body: `<div class="evidence-grid"><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>4개 활성 관절</strong><p>URDF chain의 active link와 4개 servo 명령을 확인할 수 있습니다.</p></div><div class="evidence-card"><span class="status-tag status-confirmed">CODE</span><strong>분리된 FreeRTOS task</strong><p>motion과 serial 처리를 서로 다른 core에 고정합니다.</p></div><div class="evidence-card"><span class="status-tag status-demo">DEMO</span><strong>연속 버튼 조작</strong><p>접근·정렬·누르기의 end-to-end 동작을 영상으로 확인합니다.</p></div></div>` },
    { id: 'repository', nav: 'Repository', title: 'Repository — 코드와 재현', body: `<p><a class="repo-link" href="https://github.com/jongbob1918/ROOMIE/tree/main/ros2_ws/src/roomie_ac" target="_blank" rel="noreferrer">Arm Controller 구현 보기 ↗</a></p><p>좌표변환, IK, serial manager, ESP32 펌웨어와 calibration 실행 파일이 공개되어 있습니다.</p>` }
  ]
};
