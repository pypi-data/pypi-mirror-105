import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { 
  Dialog,
  ISplashScreen, 
} from '@jupyterlab/apputils';

import { 
  Throttler 
} from '@lumino/polling';

// import { 
//   ITranslator 
// } from '@jupyterlab/translation';

import { 
  DisposableDelegate 
} from '@lumino/disposable';

/**
 * The interval in milliseconds before recover options appear during splash.
 */
const SPLASH_RECOVER_TIMEOUT = 12000;

/**
 * The command IDs used by the apputils plugin.
 */
namespace CommandIDs {
  export const loadState = 'apputils:load-statedb';

  export const print = 'apputils:print';

  export const reset = 'apputils:reset';

  export const resetOnLoad = 'apputils:reset-on-load';

  export const runFirstEnabled = 'apputils:run-first-enabled';
}


/**
 * A splash screen for epi2melabs
 */
const splash: JupyterFrontEndPlugin<ISplashScreen> = {
  id: '@epi2melabs/epi2melabs-splash:plugin',
  autoStart: true,
  // requires: [ITranslator],
  provides: ISplashScreen,
  activate: (
    app: JupyterFrontEnd
    // translator: ITranslator
  ) => {
    // const trans = translator.load('jupyterlab');
    const { 
      commands, 
      restored
    } = app;

    const splash = document.createElement('div');
    splash.id = 'epi2melabs-splash';

    const logo = document.createElement('div');
    logo.id = 'epi2melabs-logo';
    splash.appendChild(logo);

    const graphic = document.createElement('div')
    logo.appendChild(graphic)
    graphic.className = 'logoGraphic'

    const graphicTop = document.createElement('div')
    graphic.appendChild(graphicTop)
    graphicTop.className = 'graphicTop'

    const graphicMid = document.createElement('div')
    graphic.appendChild(graphicMid)
    graphicMid.className = 'graphicMid'

    const graphicBot = document.createElement('div')
    graphic.appendChild(graphicBot)
    graphicBot.className = 'graphicBot'

    const text = document.createElement('div')
    logo.appendChild(text)
    text.className = 'logoText'

    const epi2me = document.createElement('h1');
    epi2me.innerHTML = 'EPI2ME'
    text.appendChild(epi2me);

    const labs = document.createElement('h2');
    labs.innerHTML = 'Labs'
    text.appendChild(labs)

    // Create debounced recovery dialog function.
    let dialog: Dialog<unknown> | null;
    const recovery = new Throttler(
      async () => {
        if (dialog) {
          return;
        }

        dialog = new Dialog({
          title: 'Loading...',
          body: `The loading screen is taking a long time. 
Would you like to clear the workspace or keep waiting?`,
          buttons: [
            Dialog.cancelButton({ label: 'Keep Waiting' }),
            Dialog.warnButton({ label: 'Clear Workspace' })
          ]
        });

        try {
          const result = await dialog.launch();
          dialog.dispose();
          dialog = null;
          if (result.button.accept && commands.hasCommand(CommandIDs.reset)) {
            return commands.execute(CommandIDs.reset);
          }

          // Re-invoke the recovery timer in the next frame.
          requestAnimationFrame(() => {
            // Because recovery can be stopped, handle invocation rejection.
            void recovery.invoke().catch(_ => undefined);
          });
        } catch (error) {
          /* no-op */
        }
      },
      { limit: SPLASH_RECOVER_TIMEOUT, edge: 'trailing' }
    );

    // Return ISplashScreen.
    let splashCount = 0;
    return {
      show: () => {
        splash.classList.remove('splash-fade');
        splashCount++;

        console.log('adding')
        document.body.appendChild(splash);

        // Because recovery can be stopped, handle invocation rejection.
        void recovery.invoke().catch(_ => undefined);

        return new DisposableDelegate(async () => {
          await restored;
          if (--splashCount === 0) {
            void recovery.stop();

            if (dialog) {
              dialog.dispose();
              dialog = null;
            }

            splash.classList.add('splash-fade');
            window.setTimeout(() => {
              document.body.removeChild(splash);
            }, 200);
          }
        });
      }
    };
  },
};

export default splash;