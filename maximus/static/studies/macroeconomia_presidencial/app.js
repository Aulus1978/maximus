const sections = [...document.querySelectorAll('.page-section')];
const navItems = [...document.querySelectorAll('.nav-item')];
const targetButtons = [...document.querySelectorAll('[data-target]')];

function showSection(id) {
  sections.forEach(s => s.classList.toggle('active-section', s.id === id));
  navItems.forEach(n => n.classList.toggle('active', n.dataset.target === id));
  window.scrollTo({ top: 0, behavior: 'smooth' });
  localStorage.setItem('macroLastSection', id);
}
targetButtons.forEach(btn => btn.addEventListener('click', () => showSection(btn.dataset.target)));

const savedSection = localStorage.getItem('macroLastSection');
if (savedSection && document.getElementById(savedSection)) showSection(savedSection);

const flowData = {
  familias: {
    title: 'Famílias', description: 'Recebem salários, benefícios e rendimentos; consomem, pagam impostos e formam poupança.',
    inputs: 'salários, lucros, juros, benefícios', outputs: 'consumo, tributos, dívidas, poupança', risk: 'endividamento e perda de renda real',
    question: 'A renda está crescendo mais rápido ou mais devagar que os preços?'
  },
  bancos: {
    title: 'Sistema financeiro', description: 'Transforma depósitos e poupança em crédito, pagamentos e financiamento para o restante da economia.',
    inputs: 'depósitos, capital, pagamentos de dívida', outputs: 'crédito, investimentos, meios de pagamento', risk: 'inadimplência, liquidez e contágio bancário',
    question: 'O crédito está financiando produção ou apenas consumo e ativos?'
  },
  empresas: {
    title: 'Empresas', description: 'Combinam trabalho, capital e tecnologia para produzir; pagam salários e impostos e decidem quanto investir.',
    inputs: 'vendas, crédito, investimento externo', outputs: 'salários, tributos, importações, dividendos', risk: 'queda de demanda, custos e falta de financiamento',
    question: 'Por que as empresas investiriam neste país pelos próximos dez anos?'
  },
  governo: {
    title: 'Governo', description: 'Arrecada tributos, presta serviços, transfere renda, investe e se financia por meio da dívida pública.',
    inputs: 'tributos, concessões, emissão de dívida', outputs: 'serviços, salários, benefícios, investimento', risk: 'déficit persistente e gasto pouco produtivo',
    question: 'Cada despesa temporária tem fonte de financiamento e data para terminar?'
  },
  exterior: {
    title: 'Setor externo', description: 'Liga o país ao comércio, ao investimento internacional, às remessas, ao turismo e às moedas estrangeiras.',
    inputs: 'exportações, investimento direto, turismo', outputs: 'importações, juros externos, remessas', risk: 'dependência de capital volátil e moeda estrangeira',
    question: 'O déficit externo está financiando capacidade produtiva ou consumo corrente?'
  },
  bc: {
    title: 'Banco Central', description: 'Preserva a estabilidade da moeda e do sistema financeiro por meio de juros, liquidez, supervisão e reservas.',
    inputs: 'reservas, títulos, compulsórios, informação', outputs: 'liquidez, sinalização de juros, moeda', risk: 'perda de credibilidade e instabilidade financeira',
    question: 'As expectativas acreditam que a inflação voltará ao objetivo?'
  }
};

document.querySelectorAll('.flow-node').forEach(node => {
  node.addEventListener('click', () => {
    document.querySelectorAll('.flow-node').forEach(n => n.classList.remove('active'));
    node.classList.add('active');
    const d = flowData[node.dataset.node];
    document.getElementById('flowTitle').textContent = d.title;
    document.getElementById('flowDescription').textContent = d.description;
    document.getElementById('flowInputs').textContent = d.inputs;
    document.getElementById('flowOutputs').textContent = d.outputs;
    document.getElementById('flowRisk').textContent = d.risk;
    document.getElementById('flowQuestion').textContent = d.question;
  });
});

const controls = {
  interest: document.getElementById('interestRate'),
  spending: document.getElementById('publicSpending'),
  tax: document.getElementById('taxRate'),
  money: document.getElementById('moneyGrowth'),
  reserve: document.getElementById('reserveAction'),
  confidence: document.getElementById('confidence')
};

const baseline = { interest: 9.5, spending: 4, tax: 31, money: 7, reserve: 0, confidence: 55 };
const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
const fmt = (n, d=1) => n.toLocaleString('pt-BR', {minimumFractionDigits:d, maximumFractionDigits:d});

function deltaText(value, base, suffix=' p.p.') {
  const d = value - base;
  if (Math.abs(d) < .05) return 'cenário-base';
  return `${d > 0 ? '+' : '−'}${fmt(Math.abs(d))}${suffix}`;
}

function updateSimulation() {
  const i = +controls.interest.value;
  const g = +controls.spending.value;
  const t = +controls.tax.value;
  const m = +controls.money.value;
  const r = +controls.reserve.value;
  const c = +controls.confidence.value;

  document.getElementById('interestOutput').textContent = `${fmt(i)}%`;
  document.getElementById('spendingOutput').textContent = `${fmt(g)}% do PIB`;
  document.getElementById('taxOutput').textContent = `${fmt(t,0)}%`;
  document.getElementById('moneyOutput').textContent = `${fmt(m,0)}%`;
  document.getElementById('reserveOutput').textContent = r === 0 ? 'neutro' : r < 0 ? `vender US$ ${Math.abs(r)} bi` : `comprar US$ ${r} bi`;
  document.getElementById('confidenceOutput').textContent = `${fmt(c,0)} / 100`;

  const di = i - baseline.interest;
  const dg = g - baseline.spending;
  const dt = t - baseline.tax;
  const dm = m - baseline.money;
  const dc = c - baseline.confidence;

  let growth = 2.2 - di * .16 + dg * .55 - dt * .08 + dm * .06 + dc * .035 - Math.max(0,-r) * .003;
  let inflation = 5.8 - di * .24 + dg * .28 - dt * .04 + dm * .20 - dc * .018 + r * .015;
  let unemployment = 8.2 + di * .11 - dg * .25 + dt * .06 - dm * .025 - dc * .018;
  let debt = 67 + dg * 2.1 - dt * .55 + di * .20 - dc * .04 + Math.max(0,-r) * .015;
  let exchange = 4.8 - di * .045 + dg * .035 - dt * .005 + dm * .045 - dc * .018 + r * .018;
  let reserves = 120 + r;

  growth = clamp(growth, -5, 8);
  inflation = clamp(inflation, -1, 20);
  unemployment = clamp(unemployment, 3, 18);
  debt = clamp(debt, 35, 120);
  exchange = clamp(exchange, 2.5, 9);
  reserves = clamp(reserves, 20, 220);

  document.getElementById('simGrowth').textContent = `${fmt(growth)}%`;
  document.getElementById('simInflation').textContent = `${fmt(inflation)}%`;
  document.getElementById('simUnemployment').textContent = `${fmt(unemployment)}%`;
  document.getElementById('simDebt').textContent = `${fmt(debt)}%`;
  document.getElementById('simExchange').textContent = `A$ ${fmt(exchange,2)}`;
  document.getElementById('simReserves').textContent = `US$ ${fmt(reserves,0)} bi`;
  document.getElementById('deltaGrowth').textContent = deltaText(growth,2.2);
  document.getElementById('deltaInflation').textContent = deltaText(inflation,5.8);
  document.getElementById('deltaUnemployment').textContent = deltaText(unemployment,8.2);
  document.getElementById('deltaDebt').textContent = deltaText(debt,67);
  document.getElementById('deltaExchange').textContent = deltaText(exchange,4.8,'');
  document.getElementById('deltaReserves').textContent = deltaText(reserves,120,' bi');

  const scores = {
    growth: clamp(55 + growth*5 - Math.max(0,inflation-6)*2, 5, 95),
    prices: clamp(80 - Math.abs(inflation-3)*8, 5, 95),
    jobs: clamp(90 - unemployment*6, 5, 95),
    fiscal: clamp(100 - debt*.65 - Math.max(0,g-4)*4 + Math.max(0,t-31)*1.5, 5, 95),
    external: clamp(55 + (reserves-100)*.25 - Math.max(0,exchange-5)*8 + dc*.2, 5, 95)
  };
  [['Growth','growth'],['Prices','prices'],['Jobs','jobs'],['Fiscal','fiscal'],['External','external']].forEach(([id,key]) => {
    const val = Math.round(scores[key]);
    document.getElementById(`impact${id}`).style.width = `${val}%`;
    document.getElementById(`impact${id}Label`).textContent = val;
  });

  let label = 'Equilíbrio instável';
  let advice = 'Observe os efeitos cruzados: uma medida que melhora um indicador pode deteriorar outro.';
  if (inflation > 9) { label = 'Risco inflacionário'; advice = 'A demanda e a liquidez estão fortes demais para a capacidade produtiva. Combine contenção gradual com medidas de oferta e proteção focalizada.'; }
  else if (growth < 0) { label = 'Risco recessivo'; advice = 'A atividade caiu. Priorize medidas temporárias, focalizadas e com alto multiplicador, preservando a credibilidade fiscal.'; }
  else if (debt > 80) { label = 'Pressão fiscal'; advice = 'A trajetória da dívida piorou. Revise despesas permanentes, qualidade do investimento e a estrutura da arrecadação.'; }
  else if (exchange > 6) { label = 'Fragilidade cambial'; advice = 'A moeda enfraqueceu. Reservas podem suavizar volatilidade, mas confiança, inflação e contas externas precisam ser tratadas.'; }
  else if (growth > 3.2 && inflation < 5.5 && debt < 72) { label = 'Expansão equilibrada'; advice = 'O cenário combina atividade, inflação mais controlada e dívida administrável. Proteja a produtividade e evite transformar estímulos temporários em permanentes.'; }
  document.getElementById('scenarioLabel').textContent = label;
  document.getElementById('advisorText').textContent = advice;
}
Object.values(controls).forEach(control => control.addEventListener('input', updateSimulation));
document.getElementById('resetSimulation').addEventListener('click', () => {
  Object.entries(baseline).forEach(([key,value]) => controls[key].value = value);
  updateSimulation();
});
updateSimulation();

const chains = {
  interest: [
    ['Decisão','Banco Central eleva a taxa','O custo-base do dinheiro sobe.'],
    ['Mercado financeiro','Crédito e títulos ficam mais caros','Bancos recalculam empréstimos e investidores exigem retorno maior.'],
    ['Famílias e empresas','Consumo e investimento desaceleram','Compras parceladas, imóveis e projetos perdem atratividade.'],
    ['Economia real','Demanda e emprego esfriam','Empresas recebem menos pedidos e reduzem expansão.'],
    ['Resultado esperado','Inflação perde força','O efeito leva meses e depende das expectativas.']
  ],
  investment: [
    ['Decisão','Governo acelera infraestrutura','Obras, logística, energia ou saneamento recebem recursos.'],
    ['Curto prazo','Emprego e demanda aumentam','Fornecedores vendem mais e contratam.'],
    ['Médio prazo','Custos de produção caem','Estradas, energia e conectividade melhoram a eficiência.'],
    ['Financiamento','Déficit ou tributos podem subir','A qualidade da fonte importa tanto quanto a obra.'],
    ['Resultado esperado','PIB potencial cresce','O ganho depende de seleção, execução e manutenção.']
  ],
  tax: [
    ['Decisão','Imposto sobre consumo cai','O preço final pode diminuir.'],
    ['Famílias','Renda disponível aumenta','Há espaço para consumir outros bens ou poupar.'],
    ['Empresas','Vendas podem crescer','O repasse depende da concorrência.'],
    ['Governo','Arrecadação inicialmente cai','É preciso compensação, corte ou dívida.'],
    ['Resultado esperado','Atividade recebe estímulo','Pode haver inflação se a oferta não acompanhar.']
  ],
  currency: [
    ['Choque','Moeda local perde valor','Cada dólar passa a custar mais.'],
    ['Importações','Insumos e bens externos encarecem','Energia, remédios e componentes pressionam custos.'],
    ['Empresas','Exportadores ganham competitividade','Setores importadores enfrentam margens menores.'],
    ['Famílias','Inflação reduz renda real','Viagens e produtos importados ficam mais caros.'],
    ['Política econômica','Juros e reservas entram no debate','A resposta depende da causa e da intensidade.']
  ]
};
function renderChain(key) {
  document.getElementById('causalChain').innerHTML = chains[key].map((s,i) => `<article class="chain-step"><span>0${i+1} · ${s[0]}</span><strong>${s[1]}</strong><p>${s[2]}</p></article>`).join('');
}
document.querySelectorAll('.transmission-tab').forEach(btn => btn.addEventListener('click', () => {
  document.querySelectorAll('.transmission-tab').forEach(b => b.classList.remove('active'));
  btn.classList.add('active'); renderChain(btn.dataset.chain);
}));
renderChain('interest');

const crises = {
  inflation: {
    title: 'Choque de inflação com origem na oferta', brief: 'Uma seca derrubou a produção de alimentos, enquanto o petróleo subiu no exterior. A inflação anual saltou de 4% para 8%.',
    data: [['Inflação','8,0%'],['PIB','1,6%'],['Desemprego','7,9%']],
    options: [
      ['Congelar preços em toda a economia','Pode aliviar manchetes no curtíssimo prazo, mas cria escassez, mercado paralelo e desorganiza a oferta.'],
      ['Combinar proteção focalizada, política monetária crível e medidas de oferta','Resposta mais equilibrada: protege vulneráveis sem tentar esconder preços e trabalha causa, expectativas e efeitos distributivos.'],
      ['Aumentar fortemente o gasto geral para compensar a perda de renda','Pode ampliar a demanda no momento em que a oferta caiu, alimentando ainda mais a inflação.']
    ], best: 1
  },
  recession: {
    title: 'Recessão com queda do investimento privado', brief: 'A confiança despencou após uma crise externa. O PIB cai, o desemprego sobe e empresas adiam projetos.',
    data: [['PIB','−2,4%'],['Desemprego','12,1%'],['Inflação','2,2%']],
    options: [
      ['Cortar todo o gasto público imediatamente','Pode piorar a contração se o corte for abrupto e atingir investimento e proteção social.'],
      ['Usar estímulo temporário, focalizado e com plano fiscal de médio prazo','Ajuda a sustentar demanda e emprego sem abandonar a trajetória de solvência.'],
      ['Fixar por decreto metas de produção para empresas','Não resolve falta de demanda e confiança; pode gerar distorções e reduzir investimento.']
    ], best: 1
  },
  currency: {
    title: 'Fuga de capital e desvalorização rápida', brief: 'Investidores retiram recursos após incerteza política. A moeda perde 18% em poucas semanas e a inflação futura sobe.',
    data: [['Câmbio','+18%'],['Reservas','US$ 95 bi'],['Risco-país','+240 pts']],
    options: [
      ['Gastar todas as reservas para defender um valor fixo','Pode falhar e deixar o país sem proteção. Reservas servem para suavizar disfunções, não sustentar fundamentos indefinidamente.'],
      ['Restabelecer credibilidade, garantir liquidez e usar reservas de modo seletivo','Ataca o problema institucional e financeiro, reduzindo movimentos desordenados sem prometer um câmbio artificial.'],
      ['Proibir qualquer saída de capital sem plano de emergência','Controles improvisados podem agravar a desconfiança e paralisar transações legítimas.']
    ], best: 1
  },
  debt: {
    title: 'Aumento abrupto do custo da dívida pública', brief: 'A dívida vence em prazos curtos e investidores exigem juros maiores para continuar financiando o Tesouro.',
    data: [['Dívida/PIB','88%'],['Juro real','7,2%'],['Prazo médio','2,1 anos']],
    options: [
      ['Negar o problema e pressionar investidores','A comunicação hostil costuma elevar o prêmio de risco e reduzir a demanda por títulos.'],
      ['Apresentar plano crível, revisar gasto e alongar a dívida gradualmente','Combina ajuste estrutural, transparência e gestão financeira, evitando depender apenas de cortes emergenciais.'],
      ['Emitir moeda para pagar toda a dívida rapidamente','Pode transformar crise fiscal em inflação e crise cambial, especialmente sem credibilidade.']
    ], best: 1
  }
};
let activeCrisis = 'inflation';
function renderCrisis(key) {
  activeCrisis = key; const c = crises[key];
  document.getElementById('crisisTitle').textContent = c.title;
  document.getElementById('crisisBrief').textContent = c.brief;
  document.getElementById('crisisData').innerHTML = c.data.map(d => `<div><span>${d[0]}</span><strong>${d[1]}</strong></div>`).join('');
  document.getElementById('decisionOptions').innerHTML = c.options.map((o,i) => `<button class="decision-option" data-option="${i}">${o[0]}</button>`).join('');
  document.getElementById('decisionFeedback').innerHTML = '<span>Aguardando decisão presidencial.</span>';
  document.querySelectorAll('.decision-option').forEach(btn => btn.addEventListener('click', () => {
    document.querySelectorAll('.decision-option').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    const idx = +btn.dataset.option;
    document.getElementById('decisionFeedback').innerHTML = `<strong>${idx === c.best ? 'Boa primeira orientação.' : 'Alerta de gabinete.'}</strong><br>${c.options[idx][1]}`;
  }));
}
document.querySelectorAll('.crisis-card').forEach(btn => btn.addEventListener('click', () => {
  document.querySelectorAll('.crisis-card').forEach(b => b.classList.remove('active'));
  btn.classList.add('active'); renderCrisis(btn.dataset.crisis);
}));
renderCrisis('inflation');

const glossary = [
  ['Balanço de pagamentos','Registro de todas as transações entre residentes do país e o exterior.'],
  ['Câmbio','Preço de uma moeda em relação a outra.'],
  ['Conta corrente','Balanço de comércio, serviços, rendas e transferências com o exterior.'],
  ['Déficit primário','Quando despesas não financeiras superam receitas antes dos juros da dívida.'],
  ['Dívida pública','Obrigações financeiras acumuladas do governo.'],
  ['Inflação','Aumento persistente e disseminado do nível geral de preços.'],
  ['Juro real','Taxa de juros descontada a inflação esperada ou ocorrida.'],
  ['Multiplicador fiscal','Efeito total de uma mudança no gasto ou tributo sobre o PIB.'],
  ['PIB','Valor dos bens e serviços finais produzidos no território em certo período.'],
  ['PIB potencial','Nível sustentável de produção sem pressão excessiva sobre preços.'],
  ['Política fiscal','Decisões sobre receitas, despesas, transferências e dívida do governo.'],
  ['Política monetária','Decisões sobre juros e liquidez para preservar estabilidade de preços e do sistema financeiro.'],
  ['Produtividade','Quantidade produzida por unidade de trabalho, capital ou outro recurso.'],
  ['Reservas internacionais','Ativos externos líquidos mantidos pelo Banco Central.'],
  ['Resultado nominal','Resultado fiscal incluindo os juros da dívida.'],
  ['Risco-país','Prêmio exigido para investir em ativos do país em relação a referência segura.'],
  ['Senhoriagem','Receita obtida pela emissão de moeda.'],
  ['Spread bancário','Diferença entre o custo de captação dos bancos e a taxa cobrada nos empréstimos.']
];
function renderGlossary(filter='') {
  const q = filter.toLowerCase();
  document.getElementById('glossaryList').innerHTML = glossary.filter(([t,d]) => `${t} ${d}`.toLowerCase().includes(q)).map(([t,d]) => `<article class="glossary-item"><strong>${t}</strong><p>${d}</p></article>`).join('') || '<p>Nenhum termo encontrado.</p>';
}
const glossaryDialog = document.getElementById('glossaryDialog');
document.getElementById('openGlossary').addEventListener('click', () => { renderGlossary(); glossaryDialog.showModal(); });
document.getElementById('glossarySearch').addEventListener('input', e => renderGlossary(e.target.value));

const infoDialog = document.getElementById('infoDialog');
document.querySelectorAll('.explain-trigger').forEach(btn => btn.addEventListener('click', () => {
  document.getElementById('dialogTitle').textContent = 'Leia o conjunto, não a manchete';
  document.getElementById('dialogBody').innerHTML = `<p>Um painel macroeconômico funciona como os exames de um paciente. Uma taxa pode parecer boa isoladamente e ainda esconder um problema.</p><ul><li><b>PIB + inflação + desemprego</b> revelam se há recessão, ociosidade ou superaquecimento.</li><li><b>Resultado fiscal + dívida + juros</b> mostram a sustentabilidade do financiamento público.</li><li><b>Câmbio + reservas + conta corrente</b> indicam a resistência a choques externos.</li><li><b>Produtividade + renda mediana + desigualdade</b> dizem se o crescimento melhora de fato a vida da população.</li></ul>`;
  infoDialog.showModal();
}));

document.querySelectorAll('dialog .dialog-close').forEach(btn => btn.addEventListener('click', () => btn.closest('dialog').close()));
document.querySelectorAll('dialog').forEach(dialog => dialog.addEventListener('click', e => {
  const rect = dialog.getBoundingClientRect();
  if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) dialog.close();
}));

const checks = [...document.querySelectorAll('.study-check')];
function updateProgress() {
  const count = checks.filter(c => c.checked).length;
  const pct = Math.round(count / checks.length * 100);
  document.getElementById('progressBar').style.width = `${pct}%`;
  document.getElementById('progressText').textContent = `${pct}% concluído`;
  localStorage.setItem('macroProgress', JSON.stringify(checks.map(c => c.checked)));
}
const savedProgress = JSON.parse(localStorage.getItem('macroProgress') || '[]');
checks.forEach((check,i) => { check.checked = !!savedProgress[i]; check.addEventListener('change', updateProgress); });
document.getElementById('markAll').addEventListener('click', () => { checks.forEach(c => c.checked = true); updateProgress(); });
updateProgress();
