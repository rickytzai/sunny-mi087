const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

const wave = document.querySelector('#wave');
for (let i = 0; i < 29; i += 1) {
  const bar = document.createElement('i');
  bar.style.setProperty('--i', i);
  bar.style.setProperty('--h', `${12 + Math.abs(Math.sin(i * 0.72)) * 40}px`);
  wave.append(bar);
}

const stage = document.querySelector('.barge-stage');
const steps = [...stage.querySelectorAll('.flow-step')];
const progress = stage.querySelector('.flow-progress span');
let timer;

function showStep(index) {
  steps.forEach((step, i) => step.classList.toggle('active', i <= index));
  progress.style.width = `${(index + 1) * 25}%`;
  stage.dataset.step = index;
}

function playFlow() {
  clearInterval(timer);
  let index = 0;
  showStep(index);
  if (reduced) { showStep(3); return; }
  timer = setInterval(() => {
    index += 1;
    showStep(index);
    if (index === 3) clearInterval(timer);
  }, 950);
}

document.querySelector('#replay-flow').addEventListener('click', playFlow);
const stageObserver = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    playFlow();
    stageObserver.disconnect();
  }
}, { threshold: 0.35 });
stageObserver.observe(stage);
