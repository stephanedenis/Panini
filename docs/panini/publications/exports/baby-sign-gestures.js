// baby-sign-gestures.js - Bibliothèque SVG Compacte (<5KB)
// 18 gestes baby sign avec animations CSS pures

const BabySignGestures = {
  
  // === NIVEAU 1 (4-9 mois) : Primitives Cognitives ===
  
  EXIST: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-exist">
    <circle cx="30" cy="25" r="12" fill="none" stroke="#FFD700" stroke-width="3">
      <animate attributeName="stroke-opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
    </circle>
    <path d="M30,40 L30,50 M25,45 L35,45" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
  </svg>`,
  
  WANT: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-want">
    <g transform="translate(30,30)">
      <path d="M-15,-5 Q0,-15 15,-5" fill="none" stroke="#FF6B6B" stroke-width="3">
        <animate attributeName="d" values="M-15,-5 Q0,-15 15,-5;M-20,-8 Q0,-20 20,-8;M-15,-5 Q0,-15 15,-5" 
                 dur="1.5s" repeatCount="indefinite"/>
      </path>
      <circle cx="-12" cy="-2" r="3" fill="#FF6B6B"/>
      <circle cx="12" cy="-2" r="3" fill="#FF6B6B"/>
    </g>
  </svg>`,
  
  ATTEND: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-attend">
    <circle cx="30" cy="25" r="8" fill="#4ECDC4">
      <animate attributeName="r" values="6;10;6" dur="1s" repeatCount="indefinite"/>
    </circle>
    <path d="M22,25 L30,25 L38,25" stroke="#4ECDC4" stroke-width="2" opacity="0.7">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite"/>
    </path>
  </svg>`,
  
  COMM: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-comm">
    <circle cx="45" cy="20" r="6" fill="#FF9FF3"/>
    <path d="M35,25 Q40,30 45,25" fill="none" stroke="#FF9FF3" stroke-width="3">
      <animate attributeName="d" values="M35,25 Q40,30 45,25;M32,28 Q38,35 44,28;M35,25 Q40,30 45,25" 
               dur="1.2s" repeatCount="indefinite"/>
    </path>
    <circle cx="10" cy="35" r="4" fill="#FF9FF3"/>
    <path d="M15,35 L30,20" stroke="#FF9FF3" stroke-width="2" stroke-dasharray="2,2">
      <animate attributeName="stroke-dashoffset" values="0;4;0" dur="0.8s" repeatCount="indefinite"/>
    </path>
  </svg>`,
  
  MORE: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-more">
    <g transform="translate(30,30)">
      <circle cx="-8" cy="0" r="5" fill="#95E1D3">
        <animate attributeName="r" values="5;8;5" dur="1s" repeatCount="indefinite"/>
      </circle>
      <circle cx="8" cy="0" r="5" fill="#95E1D3">
        <animate attributeName="r" values="5;8;5" dur="1s" repeatCount="indefinite" begin="0.5s"/>
      </circle>
      <path d="M-3,0 L3,0" stroke="#95E1D3" stroke-width="3">
        <animate attributeName="stroke-width" values="2;5;2" dur="1s" repeatCount="indefinite"/>
      </path>
    </g>
  </svg>`,
  
  STOP: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-stop">
    <g transform="translate(30,30)">
      <path d="M-10,-10 L10,10 M10,-10 L-10,10" stroke="#FF6B6B" stroke-width="4" stroke-linecap="round">
        <animate attributeName="stroke-width" values="3;6;3" dur="0.8s" repeatCount="indefinite"/>
      </path>
      <circle cx="0" cy="0" r="15" fill="none" stroke="#FF6B6B" stroke-width="2" opacity="0.3">
        <animate attributeName="r" values="15;18;15" dur="0.8s" repeatCount="indefinite"/>
      </circle>
    </g>
  </svg>`,
  
  // === NIVEAU 2 (9-15 mois) : Opérations Conceptuelles ===
  
  POINT: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-point">
    <path d="M10,30 L45,30" stroke="#FFA726" stroke-width="4" stroke-linecap="round">
      <animate attributeName="d" values="M10,30 L45,30;M5,30 L50,30;M10,30 L45,30" 
               dur="1.5s" repeatCount="indefinite"/>
    </path>
    <polygon points="45,30 40,25 40,35" fill="#FFA726">
      <animateTransform attributeName="transform" type="translate" values="0,0;5,0;0,0" 
                        dur="1.5s" repeatCount="indefinite"/>
    </polygon>
    <circle cx="50" cy="30" r="3" fill="#FFA726" opacity="0.7">
      <animate attributeName="r" values="3;6;3" dur="1.5s" repeatCount="indefinite"/>
    </circle>
  </svg>`,
  
  ITER: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-iter">
    <g transform="translate(30,30)">
      <path d="M-12,0 A12,12 0 1,1 12,0" fill="none" stroke="#66BB6A" stroke-width="3">
        <animate attributeName="stroke-dasharray" values="0,100;75,25;0,100" dur="2s" repeatCount="indefinite"/>
      </path>
      <polygon points="12,0 8,-4 8,4" fill="#66BB6A">
        <animateTransform attributeName="transform" type="rotate" values="0;360;0" 
                          dur="2s" repeatCount="indefinite"/>
      </polygon>
    </g>
  </svg>`,
  
  DONE: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-done">
    <g transform="translate(30,30)">
      <path d="M-10,0 L-2,8 L12,-6" fill="none" stroke="#4CAF50" stroke-width="4" stroke-linecap="round">
        <animate attributeName="stroke-dasharray" values="0,30;30,0;30,0" dur="1.5s" repeatCount="indefinite"/>
      </path>
      <circle cx="0" cy="0" r="18" fill="none" stroke="#4CAF50" stroke-width="2" opacity="0.2">
        <animate attributeName="stroke-opacity" values="0.2;0.8;0.2" dur="1.5s" repeatCount="indefinite"/>
      </circle>
    </g>
  </svg>`,
  
  GO: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-go">
    <g>
      <circle cx="15" cy="30" r="4" fill="#9C27B0">
        <animateTransform attributeName="transform" type="translate" values="0,0;30,0;0,0" 
                          dur="2s" repeatCount="indefinite"/>
      </circle>
      <path d="M5,30 L50,30" stroke="#9C27B0" stroke-width="2" stroke-dasharray="5,5" opacity="0.5">
        <animate attributeName="stroke-dashoffset" values="0;10;0" dur="1s" repeatCount="indefinite"/>
      </path>
      <polygon points="50,30 45,25 45,35" fill="#9C27B0"/>
    </g>
  </svg>`,
  
  WHERE: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-where">
    <g transform="translate(30,30)">
      <circle cx="0" cy="0" r="3" fill="#FF5722">
        <animateTransform attributeName="transform" type="rotate" values="0;360;0" 
                          dur="3s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="translate" values="0,0;12,0;0,-12;-12,0;0,12;0,0" 
                          dur="3s" repeatCount="indefinite" additive="sum"/>
      </circle>
      <circle cx="0" cy="0" r="8" fill="none" stroke="#FF5722" stroke-width="1" opacity="0.5"/>
      <circle cx="0" cy="0" r="15" fill="none" stroke="#FF5722" stroke-width="1" opacity="0.3"/>
      <text x="0" y="25" text-anchor="middle" font-size="12" fill="#FF5722">?</text>
    </g>
  </svg>`,
  
  HELP: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-help">
    <g transform="translate(30,30)">
      <path d="M-8,-5 Q0,-15 8,-5" fill="none" stroke="#00BCD4" stroke-width="3"/>
      <path d="M-8,5 Q0,15 8,5" fill="none" stroke="#00BCD4" stroke-width="3"/>
      <circle cx="-6" cy="-2" r="2" fill="#00BCD4">
        <animate attributeName="cy" values="-2;2;-2" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="6" cy="-2" r="2" fill="#00BCD4">
        <animate attributeName="cy" values="-2;2;-2" dur="1.5s" repeatCount="indefinite" begin="0.75s"/>
      </circle>
    </g>
  </svg>`,
  
  // === NIVEAU 3 (15-24 mois) : Abstractions Métacognitives ===
  
  SAME_DIFF: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-same-diff">
    <g transform="translate(30,30)">
      <rect x="-15" y="-8" width="10" height="16" fill="#E91E63">
        <animate attributeName="fill" values="#E91E63;#2196F3;#E91E63" dur="2s" repeatCount="indefinite"/>
      </rect>
      <rect x="5" y="-8" width="10" height="16" fill="#2196F3">
        <animate attributeName="fill" values="#2196F3;#E91E63;#2196F3" dur="2s" repeatCount="indefinite"/>
      </rect>
      <path d="M-5,0 L5,0" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
    </g>
  </svg>`,
  
  THINK: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-think">
    <circle cx="30" cy="20" r="10" fill="none" stroke="#9E9E9E" stroke-width="2"/>
    <circle cx="25" cy="35" r="2" fill="#9E9E9E" opacity="0.7">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite"/>
    </circle>
    <circle cx="30" cy="40" r="3" fill="#9E9E9E" opacity="0.7">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite" begin="0.3s"/>
    </circle>
    <circle cx="35" cy="32" r="2.5" fill="#9E9E9E" opacity="0.7">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite" begin="0.6s"/>
    </circle>
  </svg>`,
  
  FEEL: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-feel">
    <g transform="translate(30,30)">
      <path d="M0,-10 C-6,-4 -6,4 0,10 C6,4 6,-4 0,-10" fill="#E91E63">
        <animate attributeName="fill" values="#E91E63;#FF5722;#E91E63" dur="1.5s" repeatCount="indefinite"/>
      </path>
      <circle cx="0" cy="0" r="15" fill="none" stroke="#E91E63" stroke-width="1" opacity="0.3">
        <animate attributeName="r" values="15;20;15" dur="1.5s" repeatCount="indefinite"/>
      </circle>
    </g>
  </svg>`,
  
  WHY: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-why">
    <g transform="translate(30,30)">
      <text x="0" y="5" text-anchor="middle" font-size="20" font-weight="bold" fill="#FF9800">?</text>
      <circle cx="0" cy="0" r="12" fill="none" stroke="#FF9800" stroke-width="2" stroke-dasharray="2,2">
        <animateTransform attributeName="transform" type="rotate" values="0;360;0" 
                          dur="3s" repeatCount="indefinite"/>
      </circle>
    </g>
  </svg>`,
  
  WHEN: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-when">
    <circle cx="30" cy="30" r="15" fill="none" stroke="#795548" stroke-width="3"/>
    <path d="M30,30 L30,18" stroke="#795548" stroke-width="3">
      <animateTransform attributeName="transform" type="rotate" values="0 30 30;360 30 30;0 30 30" 
                        dur="4s" repeatCount="indefinite"/>
    </path>
    <path d="M30,30 L38,30" stroke="#795548" stroke-width="2">
      <animateTransform attributeName="transform" type="rotate" values="0 30 30;360 30 30;0 30 30" 
                        dur="0.5s" repeatCount="indefinite"/>
    </path>
    <circle cx="30" cy="30" r="2" fill="#795548"/>
  </svg>`,
  
  PRETEND: `<svg viewBox="0 0 60 60" class="baby-sign baby-sign-pretend">
    <g transform="translate(30,30)">
      <circle cx="0" cy="0" r="8" fill="none" stroke="#9C27B0" stroke-width="2" stroke-dasharray="4,4">
        <animate attributeName="stroke-dasharray" values="4,4;8,2;4,4" dur="2s" repeatCount="indefinite"/>
      </circle>
      <path d="M-12,-12 Q0,-20 12,-12" fill="none" stroke="#9C27B0" stroke-width="2" opacity="0.6">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
      </path>
      <circle cx="-8" cy="-8" r="1.5" fill="#9C27B0" opacity="0.7">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite"/>
      </circle>
      <circle cx="8" cy="-8" r="1.5" fill="#9C27B0" opacity="0.7">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite" begin="0.5s"/>
      </circle>
    </g>
  </svg>`
};

// CSS d'accompagnement (ultra-compact)
const BabySignCSS = `
.baby-sign {
  width: 32px;
  height: 32px;
  display: inline-block;
  vertical-align: middle;
  margin: 0 4px;
  cursor: pointer;
  transition: transform 0.2s;
}
.baby-sign:hover {
  transform: scale(1.3);
}
.gesture-table .baby-sign {
  width: 40px;
  height: 40px;
}
`;

// Fonction d'injection
function injectBabySignGestures() {
  // Injecter CSS
  const style = document.createElement('style');
  style.textContent = BabySignCSS;
  document.head.appendChild(style);
  
  // Remplacer les placeholders
  document.querySelectorAll('[data-baby-sign]').forEach(el => {
    const gesture = el.getAttribute('data-baby-sign');
    if (BabySignGestures[gesture]) {
      el.innerHTML = BabySignGestures[gesture];
    }
  });
}

// Auto-injection
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectBabySignGestures);
} else {
  injectBabySignGestures();
}

// Export pour modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { BabySignGestures, BabySignCSS, injectBabySignGestures };
}
