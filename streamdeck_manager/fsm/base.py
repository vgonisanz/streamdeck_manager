import threading
import logging

import transitions

logger = logging.getLogger(__name__) 

class FSMBase():
    """
    Finite state machine base.

    Some states are reserved, and cannot be use for custom
    purposes or functions for all childrens of FSMBase and
    classes used as models. The names reserved are:
    
    - start: State used as initial state of the FSM.
    - wait: Function used to wait until the end of the FSM.
    - reset: Trigger function to reset the FSM.
    - run: Trigger function to start running the FSM.
    - end: State used to cleanup the FSM.

    The machine created with this class can be used in
    two ways:
    - calling wait method: Run the machine and free
    in end state with a transition.
    - calling run method: Run the machine and let execution 
    control to external classes.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._lock.acquire(blocking=False)
        self._states = ["start", "end"]
        self._machine = None

    def _append_states(self, states):
        self._states += states
    
    def _create_fsm(self, model, initial, before=None, after=None):
        """
        Create a Finite state machine to use case
        with start transition only when trigger run.
        Users can define any name except start and
        end. And must provide a valid initial value.
        """
        self._machine = transitions.Machine(
            model=model,
            states=self._states,
            initial='start'
        )
        self._machine.add_transition(
            trigger='run',
            source='start',
            dest=initial,
            before=before,
            after=after
        )
        self._machine.add_transition(
            trigger='reset',
            source='*',
            dest='start'
        )
    
    def wait(self):
        self.run()
        self._lock.acquire(blocking=True)

    def _release(self):
        """
        If user use lock with wait function, call
        this method after enter in end state with
        a transition
        """
        self._lock.release()