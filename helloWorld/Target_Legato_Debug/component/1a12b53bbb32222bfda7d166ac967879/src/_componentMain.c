/*
 * AUTO-GENERATED _componentMain.c for the helloComponent component.

 * Don't bother hand-editing this file.
 */

#include "legato.h"
#include "../liblegato/eventLoop.h"
#include "../liblegato/log.h"

#ifdef __cplusplus
extern "C" {
#endif

// Component log session variables.
le_log_SessionRef_t helloComponent_LogSession;
le_log_Level_t* helloComponent_LogLevelFilterPtr;

// Component initialization function (COMPONENT_INIT).
void _helloComponent_COMPONENT_INIT(void);

// Library initialization function.
// Will be called by the dynamic linker loader when the library is loaded.
__attribute__((constructor)) void _helloComponent_Init(void)
{
    LE_DEBUG("Initializing helloComponent component library.");

    // Register the component with the Log Daemon.
    helloComponent_LogSession = log_RegComponent("helloComponent", &helloComponent_LogLevelFilterPtr);

    //Queue the COMPONENT_INIT function to be called by the event loop
    event_QueueComponentInit(_helloComponent_COMPONENT_INIT);
}


#ifdef __cplusplus
}
#endif
