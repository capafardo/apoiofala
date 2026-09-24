"""
Script para geração e garantia de ícones/pictogramas SVG vetoriais offline do CAA-Lab.
Contém mais de 70 símbolos organizados por categorias para uso 100% autônomo e offline.
"""

import os
from pathlib import Path

PICTOGRAMS = {
    # --- FUNDAMENTAIS / INÍCIO / COMUNICAR ---
    "eu.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="30" r="16" fill="#3b82f6"/>
  <circle cx="50" cy="28" r="12" fill="#ffd1a4"/>
  <path d="M42 22 Q50 16 58 22" stroke="#2c3e50" stroke-width="4" fill="none"/>
  <circle cx="46" cy="27" r="1.5" fill="#2c3e50"/>
  <circle cx="54" cy="27" r="1.5" fill="#2c3e50"/>
  <path d="M47 33 Q50 36 53 33" stroke="#2c3e50" stroke-width="1.5" fill="none"/>
  <path d="M30 75 C30 52 70 52 70 75 Z" fill="#2563eb"/>
  <path d="M46 56 L38 68" stroke="#ffd1a4" stroke-width="5" stroke-linecap="round"/>
  <circle cx="38" cy="68" r="4" fill="#ffd1a4"/>
</svg>""",

    "quero.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 82 C20 62 10 44 10 28 C10 14 22 8 34 8 C42 8 47 13 50 18 C53 13 58 8 66 8 C78 8 90 14 90 28 C90 44 80 62 50 82 Z" fill="#ef4444" stroke="#b91c1c" stroke-width="3"/>
</svg>""",

    "sim.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="#dcfce7" stroke="#16a34a" stroke-width="4"/>
  <path d="M30 50 L44 64 L70 34" stroke="#16a34a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>""",

    "nao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="#fee2e2" stroke="#dc2626" stroke-width="4"/>
  <line x1="30" y1="30" x2="70" y2="70" stroke="#dc2626" stroke-width="10" stroke-linecap="round"/>
  <line x1="70" y1="30" x2="30" y2="70" stroke="#dc2626" stroke-width="10" stroke-linecap="round"/>
</svg>""",

    "ola.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M40 75 L40 50 C40 45 45 45 45 50 L45 35 C45 30 50 30 50 35 L50 32 C50 27 55 27 55 32 L55 35 C55 30 60 30 60 35 L60 55 C60 70 40 85 40 85 Z" fill="#fcd34d" stroke="#d97706" stroke-width="3"/>
  <path d="M68 25 Q78 35 72 45" stroke="#3b82f6" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M74 20 Q88 35 80 50" stroke="#3b82f6" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>""",

    "tchau.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M35 75 L35 50 C35 45 40 45 40 50 L40 35 C40 30 45 30 45 35 L45 32 C45 27 50 27 50 32 L50 35 C50 30 55 30 55 35 L55 55 C55 70 35 85 35 85 Z" fill="#fcd34d" stroke="#d97706" stroke-width="3" transform="rotate(-15 45 60)"/>
  <path d="M20 30 Q10 40 18 50" stroke="#ef4444" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M12 25 Q2 40 10 55" stroke="#ef4444" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>""",

    "por-favor.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M35 80 L48 35 C49 30 51 30 52 35 L65 80 Z" fill="#fcd34d" stroke="#d97706" stroke-width="3"/>
  <path d="M50 35 L50 80" stroke="#d97706" stroke-width="2"/>
  <circle cx="50" cy="20" r="8" fill="#38bdf8"/>
</svg>""",

    "obrigado.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="30" r="16" fill="#ffd1a4" stroke="#d97706" stroke-width="2"/>
  <path d="M30 80 C30 55 70 55 70 80 Z" fill="#3b82f6"/>
  <path d="M42 62 L58 62 L50 72 Z" fill="#ef4444"/>
  <path d="M44 26 Q50 30 56 26" stroke="#2c3e50" stroke-width="2" fill="none"/>
</svg>""",

    "desculpa.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="45" r="32" fill="#fef08a" stroke="#ca8a04" stroke-width="3"/>
  <circle cx="40" cy="40" r="3" fill="#854d0e"/>
  <circle cx="60" cy="40" r="3" fill="#854d0e"/>
  <path d="M40 58 Q50 48 60 58" stroke="#854d0e" stroke-width="3" fill="none"/>
  <path d="M50 78 L45 88 L55 88 Z" fill="#3b82f6"/>
</svg>""",

    "conversar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 25 C20 16 35 16 48 16 C61 16 70 23 70 32 C70 41 61 48 48 48 L35 48 L25 56 L27 46 C22 43 20 38 20 25 Z" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
  <path d="M80 50 C80 43 72 38 60 38 C48 38 40 43 40 50 C40 56 46 60 52 62 L50 70 L58 64 C68 64 80 60 80 50 Z" fill="#86efac" stroke="#16a34a" stroke-width="2"/>
</svg>""",

    "repetir.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 20 A30 30 0 1 1 20 50" fill="none" stroke="#2563eb" stroke-width="8" stroke-linecap="round"/>
  <polygon points="10,40 30,50 20,65" fill="#2563eb"/>
</svg>""",

    "gosto.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M35 50 L35 85 L20 85 L20 50 Z" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
  <path d="M35 50 C35 38 42 20 50 15 C56 12 60 16 58 25 L55 38 L80 38 C86 38 88 44 86 48 L78 80 C76 85 70 85 64 85 L35 85 Z" fill="#fcd34d" stroke="#d97706" stroke-width="3"/>
</svg>""",

    "nao-gosto.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M35 50 L35 15 L20 15 L20 50 Z" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
  <path d="M35 50 C35 62 42 80 50 85 C56 88 60 84 58 75 L55 62 L80 62 C86 62 88 56 86 52 L78 20 C76 15 70 15 64 15 L35 15 Z" fill="#fcd34d" stroke="#d97706" stroke-width="3"/>
</svg>""",

    "ajuda.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M22 65 C22 55 30 45 42 40 L52 48 L44 68 Z" fill="#fcd34d" stroke="#d97706" stroke-width="2"/>
  <path d="M78 65 C78 55 70 45 58 40 L48 48 L56 68 Z" fill="#fcd34d" stroke="#d97706" stroke-width="2"/>
  <circle cx="50" cy="30" r="10" fill="#ef4444"/>
  <line x1="45" y1="30" x2="55" y2="30" stroke="#ffffff" stroke-width="3"/>
  <line x1="50" y1="25" x2="50" y2="35" stroke="#ffffff" stroke-width="3"/>
</svg>""",

    "esperar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 20 L70 20 L55 50 L70 80 L30 80 L45 50 Z" fill="#fef08a" stroke="#ca8a04" stroke-width="3"/>
  <line x1="25" y1="20" x2="75" y2="20" stroke="#854d0e" stroke-width="4" stroke-linecap="round"/>
  <line x1="25" y1="80" x2="75" y2="80" stroke="#854d0e" stroke-width="4" stroke-linecap="round"/>
  <circle cx="50" cy="65" r="5" fill="#ca8a04"/>
</svg>""",

    "parar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <polygon points="30,10 70,10 90,30 90,70 70,90 30,90 10,70 10,30" fill="#dc2626" stroke="#991b1b" stroke-width="3"/>
  <text x="50" y="58" font-family="sans-serif" font-size="20" font-weight="900" fill="#ffffff" text-anchor="middle">PARE</text>
</svg>""",

    "ir.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M15 40 L55 40 L55 20 L88 50 L55 80 L55 60 L15 60 Z" fill="#0284c7" stroke="#0369a1" stroke-width="3"/>
</svg>""",

    # --- NECESSIDADES & CUIDADOS ---
    "banheiro.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="25" y="15" width="50" height="35" rx="5" fill="#f8fafc" stroke="#64748b" stroke-width="3"/>
  <ellipse cx="50" cy="55" rx="22" ry="12" fill="#e2e8f0" stroke="#64748b" stroke-width="3"/>
  <path d="M35 58 C35 78 65 78 65 58 Z" fill="#f8fafc" stroke="#64748b" stroke-width="3"/>
  <path d="M40 76 L36 90 L64 90 L60 76 Z" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
</svg>""",

    "xixi.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 15 C50 15 25 45 25 65 C25 80 35 90 50 90 C65 90 75 80 75 65 C75 45 50 15 50 15 Z" fill="#fef08a" stroke="#eab308" stroke-width="3"/>
  <ellipse cx="42" cy="65" rx="6" ry="10" fill="#ffffff" opacity="0.6"/>
</svg>""",

    "coco.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 20 C55 20 60 25 58 32 C68 32 75 40 72 48 C82 50 85 62 80 72 C75 82 60 85 50 85 C38 85 25 80 20 70 C15 60 20 48 30 46 C28 38 35 30 44 30 C45 25 47 20 50 20 Z" fill="#92400e" stroke="#78350f" stroke-width="3"/>
  <circle cx="42" cy="55" r="3" fill="#ffffff"/>
  <circle cx="58" cy="55" r="3" fill="#ffffff"/>
  <path d="M45 68 Q50 72 55 68" stroke="#ffffff" stroke-width="2" fill="none"/>
</svg>""",

    "dor.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="25" y="40" width="50" height="20" rx="4" fill="#fed7aa" stroke="#ea580c" stroke-width="2" transform="rotate(45 50 50)"/>
  <circle cx="50" cy="50" r="6" fill="#f97316"/>
  <path d="M50 15 L52 28 L65 24 L56 34 L68 40 L54 44 L58 56 L46 48 L40 60 L38 46 L25 48 L34 38 L22 30 L35 30 Z" fill="#ef4444" opacity="0.8"/>
</svg>""",

    "remedio.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="25" y="30" width="30" height="55" rx="4" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
  <rect x="30" y="18" width="20" height="12" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
  <rect x="32" y="48" width="16" height="16" fill="#ef4444"/>
  <path d="M60 45 C60 35 75 35 85 45 C95 55 95 70 85 80 C75 90 60 90 55 80 Z" fill="#fde047" stroke="#ca8a04" stroke-width="2"/>
  <line x1="62" y1="52" x2="82" y2="72" stroke="#ca8a04" stroke-width="2"/>
</svg>""",

    "dormir.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 60 L80 60 L80 80 L20 80 Z" fill="#3b82f6" stroke="#1d4ed8" stroke-width="3"/>
  <rect x="15" y="45" width="10" height="35" fill="#64748b"/>
  <rect x="75" y="55" width="10" height="25" fill="#64748b"/>
  <ellipse cx="35" cy="55" rx="10" ry="6" fill="#f8fafc"/>
  <path d="M60 15 C75 20 80 40 70 50 C60 45 55 30 60 15 Z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
</svg>""",

    "frio.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <line x1="50" y1="15" x2="50" y2="85" stroke="#0284c7" stroke-width="4"/>
  <line x1="15" y1="50" x2="85" y2="50" stroke="#0284c7" stroke-width="4"/>
  <line x1="25" y1="25" x2="75" y2="75" stroke="#0284c7" stroke-width="4"/>
  <line x1="75" y1="25" x2="25" y2="75" stroke="#0284c7" stroke-width="4"/>
  <circle cx="50" cy="50" r="8" fill="#bae6fd" stroke="#0284c7" stroke-width="2"/>
</svg>""",

    "calor.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="22" fill="#f59e0b" stroke="#d97706" stroke-width="3"/>
  <line x1="50" y1="10" x2="50" y2="22" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
  <line x1="50" y1="78" x2="50" y2="90" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
  <line x1="10" y1="50" x2="22" y2="50" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
  <line x1="78" y1="50" x2="90" y2="50" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
  <line x1="22" y1="22" x2="30" y2="30" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
  <line x1="70" y1="70" x2="78" y2="78" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
  <line x1="78" y1="22" x2="70" y2="30" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
  <line x1="30" y1="70" x2="22" y2="78" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
</svg>""",

    "banho.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 20 L50 20 L50 40 L35 50" fill="none" stroke="#64748b" stroke-width="4"/>
  <ellipse cx="35" cy="52" rx="14" ry="6" fill="#94a3b8"/>
  <line x1="30" y1="60" x2="25" y2="80" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
  <line x1="35" y1="60" x2="35" y2="85" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
  <line x1="40" y1="60" x2="45" y2="80" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
  <path d="M50 65 C50 60 85 60 85 75 C85 85 50 85 50 65 Z" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
</svg>""",

    "escovar-dentes.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="45" width="60" height="10" rx="3" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2" transform="rotate(-30 50 50)"/>
  <rect x="22" y="32" width="20" height="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" transform="rotate(-30 32 36)"/>
  <path d="M24 25 C30 25 35 30 40 28" stroke="#38bdf8" stroke-width="3" fill="none"/>
</svg>""",

    "trocar-roupa.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 25 L40 15 L60 15 L70 25 L85 35 L75 50 L65 42 L65 85 L35 85 L35 42 L25 50 L15 35 Z" fill="#10b981" stroke="#047857" stroke-width="3"/>
  <path d="M40 15 C45 25 55 25 60 15" stroke="#047857" stroke-width="2" fill="none"/>
</svg>""",

    "cansado.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="35" fill="#fef08a" stroke="#ca8a04" stroke-width="3"/>
  <line x1="32" y1="42" x2="44" y2="42" stroke="#854d0e" stroke-width="3" stroke-linecap="round"/>
  <line x1="56" y1="42" x2="68" y2="42" stroke="#854d0e" stroke-width="3" stroke-linecap="round"/>
  <ellipse cx="50" cy="62" rx="10" ry="14" fill="#854d0e"/>
</svg>""",

    # --- PESSOAS & FAMÍLIA ---
    "mae.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 50 C25 20 75 20 75 50 C75 75 68 85 50 85 C32 85 25 75 25 50 Z" fill="#475569"/>
  <circle cx="50" cy="48" r="22" fill="#ffd1a4"/>
  <circle cx="43" cy="45" r="2" fill="#1e293b"/>
  <circle cx="57" cy="45" r="2" fill="#1e293b"/>
  <path d="M45 56 Q50 60 55 56" stroke="#e11d48" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M30 85 C30 75 70 75 70 85 Z" fill="#ec4899"/>
</svg>""",

    "pai.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M28 35 C28 15 72 15 72 35 L72 45 C65 35 35 35 28 45 Z" fill="#1e293b"/>
  <circle cx="50" cy="48" r="22" fill="#ffd1a4"/>
  <circle cx="43" cy="45" r="2" fill="#1e293b"/>
  <circle cx="57" cy="45" r="2" fill="#1e293b"/>
  <path d="M45 56 Q50 60 55 56" stroke="#2c3e50" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M30 85 C30 72 70 72 70 85 Z" fill="#3b82f6"/>
</svg>""",

    "irmao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="35" r="18" fill="#ffd1a4"/>
  <path d="M32 28 Q50 15 68 28" stroke="#78350f" stroke-width="5" fill="none"/>
  <circle cx="44" cy="35" r="2" fill="#1e293b"/>
  <circle cx="56" cy="35" r="2" fill="#1e293b"/>
  <path d="M46 44 Q50 48 54 44" stroke="#1e293b" stroke-width="2" fill="none"/>
  <path d="M32 85 C32 60 68 60 68 85 Z" fill="#10b981"/>
</svg>""",

    "irma.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 45 C25 20 75 20 75 45" stroke="#ca8a04" stroke-width="8" fill="none"/>
  <circle cx="50" cy="35" r="18" fill="#ffd1a4"/>
  <circle cx="44" cy="35" r="2" fill="#1e293b"/>
  <circle cx="56" cy="35" r="2" fill="#1e293b"/>
  <path d="M46 44 Q50 48 54 44" stroke="#e11d48" stroke-width="2" fill="none"/>
  <path d="M32 85 C32 60 68 60 68 85 Z" fill="#f43f5e"/>
</svg>""",

    "avo-m.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="40" r="20" fill="#ffd1a4"/>
  <path d="M32 30 Q50 20 68 30" stroke="#cbd5e1" stroke-width="6" fill="none"/>
  <circle cx="42" cy="40" r="5" fill="none" stroke="#64748b" stroke-width="2"/>
  <circle cx="58" cy="40" r="5" fill="none" stroke="#64748b" stroke-width="2"/>
  <line x1="47" y1="40" x2="53" y2="40" stroke="#64748b" stroke-width="2"/>
  <path d="M30 85 C30 65 70 65 70 85 Z" fill="#64748b"/>
</svg>""",

    "avo-f.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="20" r="8" fill="#e2e8f0"/>
  <circle cx="50" cy="42" r="20" fill="#ffd1a4"/>
  <circle cx="42" cy="42" r="5" fill="none" stroke="#64748b" stroke-width="2"/>
  <circle cx="58" cy="42" r="5" fill="none" stroke="#64748b" stroke-width="2"/>
  <line x1="47" y1="42" x2="53" y2="42" stroke="#64748b" stroke-width="2"/>
  <path d="M30 85 C30 65 70 65 70 85 Z" fill="#a855f7"/>
</svg>""",

    "amigo.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="35" cy="32" r="14" fill="#ffd1a4"/>
  <path d="M20 75 C20 55 50 55 50 75 Z" fill="#3b82f6"/>
  <circle cx="65" cy="32" r="14" fill="#ffd1a4"/>
  <path d="M50 75 C50 55 80 55 80 75 Z" fill="#10b981"/>
  <path d="M35 55 Q50 65 65 55" stroke="#f59e0b" stroke-width="4" fill="none"/>
</svg>""",

    "professor.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="40" y="20" width="50" height="35" rx="3" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
  <text x="65" y="42" font-family="sans-serif" font-size="14" fill="#f8fafc" text-anchor="middle">ABC</text>
  <circle cx="28" cy="40" r="14" fill="#ffd1a4"/>
  <path d="M15 80 C15 60 40 60 40 80 Z" fill="#f59e0b"/>
  <line x1="38" y1="65" x2="50" y2="45" stroke="#ffd1a4" stroke-width="4" stroke-linecap="round"/>
</svg>""",

    "terapeuta.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="30" r="16" fill="#ffd1a4"/>
  <path d="M30 80 C30 55 70 55 70 80 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <path d="M40 50 C40 65 60 65 60 50" stroke="#0284c7" stroke-width="3" fill="none"/>
  <circle cx="50" cy="68" r="4" fill="#0284c7"/>
</svg>""",

    "familia.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="30" cy="35" r="12" fill="#ffd1a4"/>
  <path d="M15 75 C15 55 45 55 45 75 Z" fill="#3b82f6"/>
  <circle cx="70" cy="35" r="12" fill="#ffd1a4"/>
  <path d="M55 75 C55 55 85 55 85 75 Z" fill="#ec4899"/>
  <circle cx="50" cy="50" r="9" fill="#ffd1a4"/>
  <path d="M38 85 C38 70 62 70 62 85 Z" fill="#f59e0b"/>
</svg>""",

    # --- LUGARES ---
    "casa.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 15 L15 45 L25 45 L25 85 L75 85 L75 45 L85 45 Z" fill="#fbbf24" stroke="#b45309" stroke-width="3"/>
  <path d="M50 12 L10 46 L90 46 Z" fill="#dc2626" stroke="#991b1b" stroke-width="3"/>
  <rect x="42" y="55" width="16" height="30" fill="#78350f"/>
  <circle cx="54" cy="70" r="1.5" fill="#fef08a"/>
</svg>""",

    "escola.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="40" width="60" height="45" fill="#dc2626" stroke="#991b1b" stroke-width="3"/>
  <path d="M50 15 L15 42 L85 42 Z" fill="#475569" stroke="#1e293b" stroke-width="2"/>
  <circle cx="50" cy="30" r="6" fill="#fbbf24" stroke="#b45309" stroke-width="1.5"/>
  <rect x="42" y="60" width="16" height="25" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
  <rect x="26" y="50" width="10" height="10" fill="#bae6fd"/>
  <rect x="64" y="50" width="10" height="10" fill="#bae6fd"/>
</svg>""",

    "parque.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 75 L30 50 C20 48 15 35 25 25 C30 20 40 22 45 28 C50 20 65 20 70 30 C80 35 75 50 65 50 L65 75 Z" fill="#22c55e" stroke="#15803d" stroke-width="3"/>
  <rect x="42" y="50" width="12" height="35" fill="#78350f"/>
  <path d="M10 85 Q50 78 90 85" stroke="#15803d" stroke-width="4" fill="none"/>
</svg>""",

    "hospital.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="25" width="60" height="60" rx="4" fill="#f8fafc" stroke="#64748b" stroke-width="3"/>
  <rect x="42" y="35" width="16" height="40" fill="#ef4444"/>
  <rect x="30" y="47" width="40" height="16" fill="#ef4444"/>
</svg>""",

    "quarto.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="15" y="50" width="70" height="35" rx="3" fill="#3b82f6" stroke="#1d4ed8" stroke-width="3"/>
  <rect x="20" y="40" width="20" height="12" rx="2" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <path d="M75 25 L85 40 L65 40 Z" fill="#f59e0b"/>
  <line x1="75" y1="40" x2="75" y2="50" stroke="#78350f" stroke-width="3"/>
</svg>""",

    "cozinha.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="30" width="60" height="55" rx="4" fill="#e2e8f0" stroke="#64748b" stroke-width="3"/>
  <circle cx="38" cy="45" r="8" fill="#475569"/>
  <circle cx="62" cy="45" r="8" fill="#475569"/>
  <rect x="30" y="60" width="40" height="20" rx="2" fill="#1e293b"/>
</svg>""",

    "sala.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="45" width="60" height="35" rx="6" fill="#8b5cf6" stroke="#6d28d9" stroke-width="3"/>
  <rect x="15" y="55" width="12" height="25" rx="3" fill="#7c3aed"/>
  <rect x="73" y="55" width="12" height="25" rx="3" fill="#7c3aed"/>
  <line x1="28" y1="80" x2="28" y2="88" stroke="#475569" stroke-width="4"/>
  <line x1="72" y1="80" x2="72" y2="88" stroke="#475569" stroke-width="4"/>
</svg>""",

    "rua.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <polygon points="35,15 65,15 85,85 15,85" fill="#334155" stroke="#1e293b" stroke-width="2"/>
  <line x1="50" y1="20" x2="50" y2="35" stroke="#facc15" stroke-width="4"/>
  <line x1="50" y1="45" x2="50" y2="60" stroke="#facc15" stroke-width="4"/>
  <line x1="50" y1="70" x2="50" y2="85" stroke="#facc15" stroke-width="4"/>
</svg>""",

    "mercado.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 25 L30 25 L45 65 L75 65 L85 35 L35 35" fill="none" stroke="#2563eb" stroke-width="4" stroke-linecap="round"/>
  <circle cx="45" cy="78" r="6" fill="#1e293b"/>
  <circle cx="72" cy="78" r="6" fill="#1e293b"/>
  <rect x="48" y="40" width="12" height="15" fill="#ef4444"/>
  <rect x="63" y="42" width="10" height="12" fill="#10b981"/>
</svg>""",

    "praia.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M15 85 Q50 70 85 85 L85 90 L15 90 Z" fill="#fde047"/>
  <path d="M15 70 Q50 78 85 70" stroke="#0284c7" stroke-width="4" fill="none"/>
  <path d="M35 55 C35 35 65 35 65 55 Z" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
  <line x1="50" y1="40" x2="50" y2="75" stroke="#78350f" stroke-width="3"/>
</svg>""",

    # --- BRINCAR & JOGOS ---
    "bola.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="36" fill="#ffffff" stroke="#1e293b" stroke-width="3"/>
  <polygon points="50,35 62,44 58,58 42,58 38,44" fill="#1e293b"/>
  <line x1="50" y1="35" x2="50" y2="15" stroke="#1e293b" stroke-width="2"/>
  <line x1="62" y1="44" x2="80" y2="38" stroke="#1e293b" stroke-width="2"/>
  <line x1="58" y1="58" x2="72" y2="76" stroke="#1e293b" stroke-width="2"/>
  <line x1="42" y1="58" x2="28" y2="76" stroke="#1e293b" stroke-width="2"/>
  <line x1="38" y1="44" x2="20" y2="38" stroke="#1e293b" stroke-width="2"/>
</svg>""",

    "boneca.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="30" r="14" fill="#ffd1a4"/>
  <path d="M35 25 C35 15 65 15 65 25" stroke="#ca8a04" stroke-width="6" fill="none"/>
  <path d="M32 80 L40 45 L60 45 L68 80 Z" fill="#ec4899" stroke="#be185d" stroke-width="2"/>
  <circle cx="45" cy="30" r="1.5" fill="#1e293b"/>
  <circle cx="55" cy="30" r="1.5" fill="#1e293b"/>
  <path d="M47 36 Q50 39 53 36" stroke="#e11d48" stroke-width="1.5" fill="none"/>
</svg>""",

    "carrinho.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 60 L25 45 L45 40 L65 40 L75 50 L85 55 L85 68 L20 68 Z" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
  <circle cx="35" cy="70" r="10" fill="#334155" stroke="#0f172a" stroke-width="2"/>
  <circle cx="70" cy="70" r="10" fill="#334155" stroke="#0f172a" stroke-width="2"/>
  <rect x="45" y="44" width="16" height="10" fill="#bae6fd"/>
</svg>""",

    "blocos.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="55" width="30" height="30" rx="3" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
  <rect x="52" y="55" width="30" height="30" rx="3" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
  <rect x="36" y="24" width="30" height="30" rx="3" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
</svg>""",

    "desenhar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="25" y="20" width="50" height="65" rx="3" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
  <path d="M60 25 L75 40 L45 70 L30 70 L30 55 Z" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
  <polygon points="30,70 30,60 40,70" fill="#1e293b"/>
</svg>""",

    "quebra-cabeca.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 30 L45 30 C45 24 55 24 55 30 L70 30 L70 45 C76 45 76 55 70 55 L70 70 L55 70 C55 76 45 76 45 70 L30 70 L30 55 C24 55 24 45 30 45 Z" fill="#38bdf8" stroke="#0284c7" stroke-width="3"/>
</svg>""",

    "tablet.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="20" width="60" height="65" rx="6" fill="#1e293b" stroke="#0f172a" stroke-width="3"/>
  <rect x="26" y="26" width="48" height="48" rx="2" fill="#38bdf8"/>
  <circle cx="50" cy="79" r="3" fill="#94a3b8"/>
  <polygon points="46,42 58,50 46,58" fill="#ffffff"/>
</svg>""",

    "musica.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="35" cy="70" r="10" fill="#a855f7"/>
  <circle cx="70" cy="60" r="10" fill="#a855f7"/>
  <rect x="42" y="30" width="5" height="40" fill="#9333ea"/>
  <rect x="77" y="20" width="5" height="40" fill="#9333ea"/>
  <polygon points="42,30 82,20 82,30 42,40" fill="#9333ea"/>
</svg>""",

    "correr.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="65" cy="25" r="10" fill="#ffd1a4"/>
  <path d="M58 35 L45 55 L30 50" stroke="#3b82f6" stroke-width="6" stroke-linecap="round" fill="none"/>
  <path d="M45 55 L60 65 L45 85" stroke="#1d4ed8" stroke-width="6" stroke-linecap="round" fill="none"/>
  <path d="M60 40 L75 50 L90 45" stroke="#ffd1a4" stroke-width="4" stroke-linecap="round" fill="none"/>
</svg>""",

    "brincar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="38" fill="#f8fafc" stroke="#0f172a" stroke-width="3"/>
  <path d="M50 12 A38 38 0 0 1 88 50 L50 50 Z" fill="#ef4444"/>
  <path d="M88 50 A38 38 0 0 1 50 88 L50 50 Z" fill="#3b82f6"/>
  <path d="M50 88 A38 38 0 0 1 12 50 L50 50 Z" fill="#eab308"/>
  <path d="M12 50 A38 38 0 0 1 50 12 L50 50 Z" fill="#10b981"/>
  <circle cx="50" cy="50" r="8" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
</svg>""",

    # --- MAIS & CONCEITOS ---
    "mais.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="42" y="15" width="16" height="70" rx="6" fill="#8b5cf6"/>
  <rect x="15" y="42" width="70" height="16" rx="6" fill="#8b5cf6"/>
</svg>""",

    "menos.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="15" y="42" width="70" height="16" rx="6" fill="#8b5cf6"/>
</svg>""",

    "rapido.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <polygon points="55,15 25,55 48,55 42,85 75,45 52,45" fill="#facc15" stroke="#ca8a04" stroke-width="3"/>
</svg>""",

    "devagar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 60 C25 40 45 30 65 30 C75 30 80 40 80 60 Z" fill="#15803d" stroke="#166534" stroke-width="3"/>
  <circle cx="82" cy="55" r="8" fill="#86efac"/>
  <circle cx="30" cy="65" r="5" fill="#15803d"/>
  <circle cx="65" cy="65" r="5" fill="#15803d"/>
</svg>""",

    "agora.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="35" fill="#f8fafc" stroke="#2563eb" stroke-width="4"/>
  <line x1="50" y1="50" x2="50" y2="25" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/>
  <line x1="50" y1="50" x2="68" y2="50" stroke="#1e293b" stroke-width="4" stroke-linecap="round"/>
  <circle cx="50" cy="50" r="4" fill="#ef4444"/>
</svg>""",

    "depois.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="25" width="60" height="55" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="3"/>
  <rect x="20" y="25" width="60" height="15" fill="#3b82f6"/>
  <path d="M40 55 L55 55 L55 45 L70 60 L55 75 L55 65 L40 65 Z" fill="#10b981"/>
</svg>""",

    "grande.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="35" fill="#38bdf8" stroke="#0284c7" stroke-width="4"/>
  <text x="50" y="56" font-family="sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">G</text>
</svg>""",

    "pequeno.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="16" fill="#f43f5e" stroke="#be185d" stroke-width="3"/>
  <text x="50" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">P</text>
</svg>""",

    "bonito.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <polygon points="50,15 61,38 86,41 68,59 72,84 50,72 28,84 32,59 14,41 39,38" fill="#facc15" stroke="#ca8a04" stroke-width="3"/>
</svg>""",

    "abrir.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="15" width="60" height="70" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
  <polygon points="20,15 65,25 65,85 20,85" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
  <circle cx="58" cy="55" r="2.5" fill="#ffffff"/>
</svg>""",

    "fechar.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="20" y="15" width="60" height="70" fill="#f59e0b" stroke="#b45309" stroke-width="3"/>
  <circle cx="70" cy="55" r="3" fill="#78350f"/>
</svg>""",

    # --- COMIDA E BEBIDA ---
    "agua.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 20 L36 85 C36 88 42 90 50 90 C58 90 64 88 64 85 L70 20 Z" fill="#bae6fd" stroke="#0284c7" stroke-width="3"/>
  <path d="M34 45 C42 42 48 48 56 45 C60 43 64 45 66 45 L63 85 C63 87 58 88 50 88 C42 88 37 87 37 85 Z" fill="#38bdf8"/>
</svg>""",

    "beber.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 25 L38 85 C38 88 42 90 50 90 C58 90 62 88 62 85 L70 25 Z" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
  <path d="M34 50 L66 50 L63 80 C63 82 58 84 50 84 C42 84 37 82 37 80 Z" fill="#38bdf8"/>
  <path d="M52 10 L48 40 L60 8" stroke="#f59e0b" stroke-width="4" stroke-linecap="round" fill="none"/>
  <ellipse cx="50" cy="25" rx="20" ry="4" fill="none" stroke="#0284c7" stroke-width="2"/>
</svg>""",

    "suco.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M30 20 L36 85 C36 88 42 90 50 90 C58 90 64 88 64 85 L70 20 Z" fill="#ffedd5" stroke="#ea580c" stroke-width="3"/>
  <path d="M34 45 L66 45 L63 85 C63 87 58 88 50 88 C42 88 37 87 37 85 Z" fill="#f97316"/>
  <path d="M52 10 L48 40 L60 8" stroke="#16a34a" stroke-width="4" stroke-linecap="round" fill="none"/>
</svg>""",

    "leite.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="30" y="35" width="40" height="55" rx="3" fill="#f8fafc" stroke="#0284c7" stroke-width="3"/>
  <path d="M30 35 L40 18 L60 18 L70 35 Z" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
  <rect x="30" y="50" width="40" height="20" fill="#38bdf8"/>
  <text x="50" y="65" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">LEITE</text>
</svg>""",

    "pao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M15 55 C15 35 35 25 60 25 C75 25 88 35 88 50 C88 65 75 75 55 75 C30 75 15 70 15 55 Z" fill="#f59e0b" stroke="#b45309" stroke-width="3"/>
  <path d="M30 40 Q40 50 45 60" stroke="#78350f" stroke-width="3" stroke-linecap="round" fill="none"/>
  <path d="M50 35 Q60 45 65 55" stroke="#78350f" stroke-width="3" stroke-linecap="round" fill="none"/>
  <path d="M70 38 Q78 48 80 55" stroke="#78350f" stroke-width="3" stroke-linecap="round" fill="none"/>
</svg>""",

    "comer.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50 35 C40 20 20 25 20 48 C20 75 45 88 50 88 C55 88 80 75 80 48 C80 25 60 20 50 35 Z" fill="#ef4444" stroke="#991b1b" stroke-width="3"/>
  <path d="M50 35 Q50 15 62 12" stroke="#78350f" stroke-width="4" fill="none" stroke-linecap="round"/>
  <ellipse cx="64" cy="18" rx="8" ry="4" fill="#22c55e" transform="rotate(-30 64 18)"/>
</svg>""",

    "arroz.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 50 C20 75 80 75 80 50 Z" fill="#f1f5f9" stroke="#64748b" stroke-width="3"/>
  <path d="M20 50 C20 38 40 30 50 30 C60 30 80 38 80 50 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <ellipse cx="45" cy="40" rx="3" ry="1.5" fill="#94a3b8"/>
  <ellipse cx="55" cy="42" rx="3" ry="1.5" fill="#94a3b8"/>
  <ellipse cx="50" cy="46" rx="3" ry="1.5" fill="#94a3b8"/>
</svg>""",

    "feijao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M20 50 C20 75 80 75 80 50 Z" fill="#78350f" stroke="#451a03" stroke-width="3"/>
  <path d="M20 50 C20 38 40 30 50 30 C60 30 80 38 80 50 Z" fill="#92400e" stroke="#451a03" stroke-width="2"/>
  <ellipse cx="40" cy="42" rx="4" ry="2.5" fill="#451a03"/>
  <ellipse cx="52" cy="38" rx="4" ry="2.5" fill="#451a03"/>
  <ellipse cx="62" cy="44" rx="4" ry="2.5" fill="#451a03"/>
</svg>""",

    "carne.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 45 C15 30 35 15 55 25 C75 35 85 55 75 70 C65 85 35 85 25 70 C18 60 18 50 25 45 Z" fill="#ef4444" stroke="#991b1b" stroke-width="3"/>
  <ellipse cx="42" cy="48" rx="8" ry="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
</svg>""",

    "fruta.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M25 70 C20 50 35 25 55 35 C70 45 50 80 30 80 C26 80 25 75 25 70 Z" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
  <path d="M35 75 C55 80 80 65 85 40 C86 35 82 35 80 38 C75 55 55 68 35 68 Z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
  <path d="M50 35 Q52 20 60 18" stroke="#15803d" stroke-width="3" stroke-linecap="round" fill="none"/>
</svg>""",

    # --- SENTIMENTOS ---
    "feliz.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="38" fill="#fef08a" stroke="#ca8a04" stroke-width="3"/>
  <circle cx="38" cy="42" r="4" fill="#854d0e"/>
  <circle cx="62" cy="42" r="4" fill="#854d0e"/>
  <path d="M34 56 Q50 74 66 56" stroke="#854d0e" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>""",

    "triste.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="38" fill="#bae6fd" stroke="#0284c7" stroke-width="3"/>
  <circle cx="38" cy="44" r="4" fill="#0369a1"/>
  <circle cx="62" cy="44" r="4" fill="#0369a1"/>
  <path d="M34 66 Q50 50 66 66" stroke="#0369a1" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>""",
}


def ensure_pictograms(base_dir: Path = None):
    """Garante a presença dos arquivos SVG nas pastas static e assets.

    Escreve apenas pictogramas ausentes e tolera diretórios somente leitura
    (ex.: instalação empacotada em /opt), onde os SVGs já são embarcados.
    """
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent.parent

    target_dirs = [
        base_dir / "app" / "static" / "pictograms",
        base_dir / "assets" / "pictograms",
    ]

    for t_dir in target_dirs:
        try:
            t_dir.mkdir(parents=True, exist_ok=True)
            for filename, svg_content in PICTOGRAMS.items():
                file_path = t_dir / filename
                if not file_path.exists():
                    file_path.write_text(svg_content.strip(), encoding="utf-8")
        except OSError:
            # Diretório não gravável (instalação em /opt) — SVGs já embarcados
            continue


if __name__ == "__main__":
    ensure_pictograms()
    print(f"Gerados {len(PICTOGRAMS)} pictogramas com sucesso.")
