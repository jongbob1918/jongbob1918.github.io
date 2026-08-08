export const categories = [
  {
    id: 'robotics-foundations',
    number: '01',
    title: '로봇공학 기초',
    description: '로봇을 표현하고 분석하는 데 필요한 수학과 시스템의 기본 원리를 다룹니다.',
    topics: ['좌표계·좌표변환', '회전행렬·Quaternion', '선형대수·확률', 'Kinematics·Dynamics', '상태·Feedback·안정성'],
    children: [
      { id: 'coordinate-transform', title: '좌표·변환' },
      { id: 'kinematics', title: 'Kinematics' },
      { id: 'dynamics-control', title: 'Dynamics·Control' }
    ]
  },
  {
    id: 'localization-slam',
    number: '02',
    title: '위치추정·SLAM',
    description: '센서 관측으로 로봇의 상태와 환경 지도를 추정하는 방법을 다룹니다.',
    topics: ['LiDAR·Camera·IMU', '시간 동기화', 'Odometry', 'Sensor Fusion', 'Scan Matching', 'Localization·Mapping'],
    children: [
      { id: 'odometry', title: 'Odometry' },
      { id: 'sensor-fusion', title: 'Sensor Fusion' },
      { id: 'mapping-loop-closure', title: 'Mapping·Loop Closure' }
    ]
  },
  {
    id: 'planning-control',
    number: '03',
    title: '경로계획·제어',
    description: '목표까지의 경로를 생성하고 실제 로봇이 안정적으로 추종하게 만드는 방법을 다룹니다.',
    topics: ['Map·Costmap', 'A*·Dijkstra', 'Global·Local Planning', 'Traversability', 'Path Tracking', 'PID·DWA·MPPI·MPC'],
    children: [
      { id: 'global-planning', title: 'Global Planning' },
      { id: 'local-planning', title: 'Local Planning' },
      { id: 'motion-control', title: 'Motion Control' }
    ]
  },
  {
    id: 'ros2-systems',
    number: '04',
    title: 'ROS 2·로봇 시스템',
    description: '로봇 알고리즘을 분산 시스템으로 구성하고 운영하는 기술을 다룹니다.',
    topics: ['Node·Topic·Action', 'Executor·QoS·DDS', 'tf2·rosbag', 'Launch·Lifecycle', 'Linux·Docker·Network', 'Jetson·배포·모니터링'],
    children: [
      { id: 'ros2-core', title: 'ROS 2 Core' },
      { id: 'navigation2', title: 'Navigation2' },
      { id: 'deployment', title: 'Deployment' }
    ]
  },
  {
    id: 'projects',
    number: '05',
    title: '프로젝트',
    description: '로봇 소프트웨어 프로젝트의 설계, 구현, 검증 내용을 정리합니다.',
    topics: ['JAVIS', 'ROOMIE', 'FALCON'],
    children: [
      { id: 'javis', title: 'JAVIS' },
      { id: 'roomie', title: 'ROOMIE' },
      { id: 'falcon', title: 'FALCON' }
    ]
  }
] as const;

export const categoryMap = new Map(categories.map(category => [category.id, category]));

export type CategoryId = typeof categories[number]['id'];

export const contentTypeLabels = {
  overview: '개요',
  concept: '개념',
  algorithm: '알고리즘',
  implementation: '구현',
  experiment: '실험',
  'case-study': '사례 분석'
} as const;
