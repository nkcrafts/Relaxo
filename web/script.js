const storageKey = 'focus-forge-state';

const goalInput = document.getElementById('goalInput');
const categorySelect = document.getElementById('categorySelect');
const addGoalButton = document.getElementById('addGoalButton');
const resetBoardButton = document.getElementById('resetBoardButton');
const goalList = document.getElementById('goalList');
const statusText = document.getElementById('statusText');
const goalCount = document.getElementById('goalCount');
const doneCount = document.getElementById('doneCount');
const sessionCount = document.getElementById('sessionCount');
const sessionMinutes = document.getElementById('sessionMinutes');
const activeGoalLabel = document.getElementById('activeGoalLabel');
const timerText = document.getElementById('timerText');
const tipText = document.getElementById('tipText');
const startButton = document.getElementById('startButton');
const pauseButton = document.getElementById('pauseButton');
const resetTimerButton = document.getElementById('resetTimerButton');

const defaultState = {
    goals: [
        { id: crypto.randomUUID(), title: 'Set up first GitHub repo', category: 'Project', done: false },
        { id: crypto.randomUUID(), title: 'Write a short README', category: 'Project', done: false },
    ],
    activeGoalId: null,
    sessionMinutes: 25,
    remainingSeconds: 25 * 60,
    sessionsCompleted: 0,
    isRunning: false,
};

let state = loadState();
let timerId = null;

function loadState() {
    try {
        const saved = JSON.parse(localStorage.getItem(storageKey));
        if (!saved || typeof saved !== 'object') {
            return structuredClone(defaultState);
        }

        return {
            ...structuredClone(defaultState),
            ...saved,
            goals: Array.isArray(saved.goals) ? saved.goals : structuredClone(defaultState).goals,
            sessionMinutes: Number(saved.sessionMinutes) || defaultState.sessionMinutes,
            remainingSeconds: Number(saved.remainingSeconds) || defaultState.remainingSeconds,
            sessionsCompleted: Number(saved.sessionsCompleted) || 0,
            isRunning: false,
        };
    } catch {
        return structuredClone(defaultState);
    }
}

function saveState() {
    localStorage.setItem(storageKey, JSON.stringify({
        goals: state.goals,
        activeGoalId: state.activeGoalId,
        sessionMinutes: state.sessionMinutes,
        remainingSeconds: state.remainingSeconds,
        sessionsCompleted: state.sessionsCompleted,
    }));
}

function formatTime(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function setStatus(message) {
    statusText.textContent = message;
}

function setTip(message) {
    tipText.textContent = message;
}

function getActiveGoal() {
    return state.goals.find((goal) => goal.id === state.activeGoalId) || null;
}

function renderStats() {
    goalCount.textContent = String(state.goals.length);
    doneCount.textContent = String(state.goals.filter((goal) => goal.done).length);
    sessionCount.textContent = String(state.sessionsCompleted);
}

function renderTimer() {
    timerText.textContent = formatTime(state.remainingSeconds);
    sessionMinutes.value = String(state.sessionMinutes);

    const activeGoal = getActiveGoal();
    activeGoalLabel.textContent = activeGoal
        ? `Active goal: ${activeGoal.title}`
        : 'No active goal selected';

    if (state.isRunning) {
        setTip('Stay with the current task. One clean sprint beats ten half-starts.');
    } else if (state.remainingSeconds === state.sessionMinutes * 60) {
        setTip('Pick one goal, then press Start to begin a clean sprint.');
    }
}

function renderGoals() {
    goalList.innerHTML = '';

    if (state.goals.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'Add a goal above to start building your board.';
        goalList.appendChild(emptyState);
        return;
    }

    state.goals.forEach((goal) => {
        const card = document.createElement('article');
        card.className = `goal-card${goal.done ? ' done' : ''}${goal.id === state.activeGoalId ? ' active' : ''}`;

        const title = document.createElement('h3');
        title.textContent = goal.title;

        const meta = document.createElement('p');
        meta.className = 'goal-meta';
        meta.textContent = goal.category;

        const actions = document.createElement('div');
        actions.className = 'goal-actions';

        const selectButton = document.createElement('button');
        selectButton.type = 'button';
        selectButton.className = 'ghost-button';
        selectButton.textContent = goal.id === state.activeGoalId ? 'Selected' : 'Set active';
        selectButton.disabled = goal.done;
        selectButton.addEventListener('click', () => {
            state.activeGoalId = goal.id;
            setStatus(`Working on ${goal.title}.`);
            updateView();
        });

        const doneButton = document.createElement('button');
        doneButton.type = 'button';
        doneButton.className = 'primary-button';
        doneButton.textContent = goal.done ? 'Undo' : 'Done';
        doneButton.addEventListener('click', () => {
            goal.done = !goal.done;
            if (goal.done && state.activeGoalId === goal.id) {
                state.activeGoalId = null;
            }
            setStatus(goal.done ? `${goal.title} marked complete.` : `${goal.title} moved back to the board.`);
            updateView();
        });

        const deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.className = 'ghost-button danger';
        deleteButton.textContent = 'Remove';
        deleteButton.addEventListener('click', () => {
            state.goals = state.goals.filter((item) => item.id !== goal.id);
            if (state.activeGoalId === goal.id) {
                state.activeGoalId = null;
            }
            setStatus('Goal removed from the board.');
            updateView();
        });

        actions.append(selectButton, doneButton, deleteButton);
        card.append(title, meta, actions);
        goalList.appendChild(card);
    });
}

function updateView() {
    renderGoals();
    renderStats();
    renderTimer();
    saveState();
}

function addGoal() {
    const title = goalInput.value.trim();

    if (!title) {
        setStatus('Type a goal first.');
        goalInput.focus();
        return;
    }

    const goal = {
        id: crypto.randomUUID(),
        title,
        category: categorySelect.value,
        done: false,
    };

    state.goals = [goal, ...state.goals];
    state.activeGoalId = goal.id;
    goalInput.value = '';
    setStatus(`Added ${title} and selected it as the active goal.`);
    updateView();
}

function syncSessionLength() {
    const value = Number(sessionMinutes.value);
    if (!Number.isFinite(value) || value < 5) {
        sessionMinutes.value = String(state.sessionMinutes);
        return;
    }

    state.sessionMinutes = Math.min(Math.max(Math.round(value), 5), 120);
    if (!state.isRunning) {
        state.remainingSeconds = state.sessionMinutes * 60;
    }
    updateView();
}

function startTimer() {
    syncSessionLength();

    if (state.goals.length === 0) {
        setStatus('Add at least one goal before starting.');
        return;
    }

    if (state.isRunning) {
        return;
    }

    if (state.remainingSeconds <= 0) {
        state.remainingSeconds = state.sessionMinutes * 60;
    }

    state.isRunning = true;
    setStatus('Focus session started.');
    clearInterval(timerId);
    timerId = setInterval(tick, 1000);
    updateView();
}

function pauseTimer() {
    if (!state.isRunning) {
        setStatus('Timer is already paused.');
        return;
    }

    state.isRunning = false;
    clearInterval(timerId);
    timerId = null;
    setStatus('Session paused.');
    updateView();
}

function resetTimer() {
    state.isRunning = false;
    clearInterval(timerId);
    timerId = null;
    state.remainingSeconds = state.sessionMinutes * 60;
    setStatus('Timer reset.');
    updateView();
}

function tick() {
    if (state.remainingSeconds <= 1) {
        state.remainingSeconds = 0;
        finishSession();
        return;
    }

    state.remainingSeconds -= 1;
    updateView();
}

function finishSession() {
    state.isRunning = false;
    clearInterval(timerId);
    timerId = null;
    state.sessionsCompleted += 1;
    setStatus('Session complete. Pick the next goal and keep the streak alive.');
    setTip('Take a short break, then come back while the task is still warm.');
    updateView();
}

function resetBoard() {
    if (!confirm('Reset the board and remove all saved goals?')) {
        return;
    }

    state = structuredClone(defaultState);
    clearInterval(timerId);
    timerId = null;
    setStatus('Board reset. Add a fresh goal to begin.');
    updateView();
}

addGoalButton.addEventListener('click', addGoal);
resetBoardButton.addEventListener('click', resetBoard);
startButton.addEventListener('click', startTimer);
pauseButton.addEventListener('click', pauseTimer);
resetTimerButton.addEventListener('click', resetTimer);
sessionMinutes.addEventListener('change', syncSessionLength);
goalInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        addGoal();
    }
});

window.addEventListener('beforeunload', () => {
    if (timerId) {
        clearInterval(timerId);
    }
    saveState();
});

updateView();
