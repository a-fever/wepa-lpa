const electron = require('electron')
// Module to control application life.
const app = electron.app
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow

const path = require('path')
const Menu = electron.Menu
const Tray = electron.Tray

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow
let appIcon = null

if (process.platform === 'linux') {
    app.disableHardwareAcceleration();
}

// To make the app as single instance application
if (!app.requestSingleInstanceLock()) {
    console.error("[ERROR] multiple instance of app is not allowed.")
    return app.quit()
}

// Register the wepa-lpa deep link.
if (process.defaultApp) {
    console.log('Process is default app.');
    if (process.argv.length >= 2) {
        console.log('Process arguments >= 2 detected.');
        app.setAsDefaultProtocolClient('wepa-lpa', process.execPath, [path.resolve(process.argv[1])])
    } else {
        console.log('Too few process arguments.');
    }
} else {
    console.log('Process is not default app.');
    app.setAsDefaultProtocolClient('wepa-lpa')
}

function createWindow(isCalledViaCli) {
    console.log('Creating LPA app window...')

    // Primary application instance
    const appiconPath = process.platform === 'win32' ? '/favicon.ico' : '/images/favicon.png'

    if (isCalledViaCli) {
        console.log('App invoked as non GUI.')
        // Create the browser window.
        mainWindow = new BrowserWindow({width: 350, height: 459, show: false})
        // Define CLI parameter in global object
        global.sharedObject = {isCli: 1} // 0 - GUI, 1 - No GUI
    } else {
        console.log('App invoked as GUI.')
        // Create the browser window.
        mainWindow = new BrowserWindow({width: 350, height: 459, resizable: false, show: false, icon: __dirname + appiconPath}) // Older dimensions - 1050 x 800
        // Define CLI parameter in global object
        global.sharedObject = {isCli: 0} // 0 - GUI, 1 - No GUI
    }

    const iconName = process.platform === 'win32' ? 'menu_icon.ico' : 'Icon32.png'
    const iconPath = path.join(__dirname, iconName)
    appIcon = new Tray(iconPath)
    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Open',
            click: function () {
                winMaximize()
            }
        },
        {
            label: 'Quit',
            click: function () {
                appClose()
            }
        }
    ])
    appIcon.setToolTip('wepa Print App')
    appIcon.setContextMenu(contextMenu)

    // To hide the application after minimized
    mainWindow.on('minimize', function (event) {
        event.preventDefault();
        mainWindow.hide();
    });

    // To prevent application from closing and hide the application to reopen it from system tray
    mainWindow.on('close', function (event) {
        if (!app.isQuiting) {
            event.preventDefault();
            mainWindow.hide();
        }
        return false;
    });

    // and load the index.html of the app.
    mainWindow.loadURL('file://' + __dirname + '/index.html')
    console.log('LPA Angular components loaded.')

    mainWindow.once('ready-to-show', function () {
        if (isCalledViaCli) {
            mainWindow.hide()
        } else {
            mainWindow.show()
            // Open the DevTools.
            // mainWindow.webContents.openDevTools()
        }
    })
}

function checkIfCalledViaCLI(args) {
    if (args && args.length > 1) {
        return true;
    }
    return false;
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', function () {

    // Check whether the app opening as GUI/Non GUI
    let isCalledViaCLI = checkIfCalledViaCLI(process.argv);
    if (isCalledViaCLI) {
        console.log('App invoked as non GUI mode.')
        createWindow(true)
    } else {
        console.log('App invoked as GUI mode.')
        createWindow(false)
    }
})

app.on('second-instance', (event, commandLine, workingDirectory) => {
    // Second instance detected. We should focus the main window and see if there's a wepa-lpa scheme call.
    console.log('Second instance event fired. Will process accordingly.');
    if (mainWindow) {
        if (mainWindow.isMinimized()) {
            console.log('Main window minimized. Restoring.');
            mainWindow.restore()
        }
        console.log('Focusing main window.');
        mainWindow.focus()
    }
    
    const arg = commandLine[commandLine.length - 1];
    if (arg.startsWith('wepa-lpa://')) {
    	handleDeepLink(commandLine[commandLine.length - 1]);
    }
})

// Handle the deep link protocol.
function handleDeepLink(urlString) {
    console.log(`App invoked from the "wepa-lpa" protocol.`)

    const url = new URL(urlString);
    
    // If no match, the URL is invalid, and we will not process.
    if (!url.searchParams.has('u-cookie') || !url.searchParams.has('u-email')) {
        console.log('The URL received does not meet the login requirements. Will not process the request.');
    	return;
    }
    
    const email = url.searchParams.get('u-email');
    const cookie = url.searchParams.get('u-cookie');
    console.log(`Email found in the requesting URL: [${email}]`);
    mainWindow.webContents.send('external-login', email, cookie);
}

function winMaximize() {
    mainWindow.restore()
    mainWindow.show()
    mainWindow.focus()
}

function appClose() {
    app.isQuiting = true;
    mainWindow.destroy()
    appIcon.destroy()
    app.quit()
}
