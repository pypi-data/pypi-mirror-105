import { AppBar, Toolbar } from '@material-ui/core';
import React, { useCallback } from 'react';
import HitherJobMonitorControl from './HitherJobMonitorControl';
import ServerStatusControl from './ServerStatusControl';
import SettingsControl from './SettingsControl';
const appBarHeight = 50;
const homeButtonStyle = {
    paddingBottom: 0, color: 'white', fontFamily: 'sans-serif', fontWeight: 'bold',
    cursor: 'pointer'
};
const ApplicationBar = ({ onOpenSettings, onOpenJobMonitor, workspaceRouteDispatch, logo }) => {
    const handleHome = useCallback(() => {
        workspaceRouteDispatch({ type: 'gotoRecordingsPage' });
    }, [workspaceRouteDispatch]);
    return (React.createElement(AppBar, { position: "static", style: { height: appBarHeight, color: 'white' } },
        React.createElement(Toolbar, null,
            logo && (React.createElement("img", { src: logo, className: "App-logo", alt: "logo", height: 30, style: { paddingBottom: 5, cursor: 'pointer' }, onClick: handleHome })),
            "\u00A0\u00A0\u00A0",
            React.createElement("div", { style: homeButtonStyle, onClick: handleHome }, "Labbox Ephys"),
            React.createElement("span", { style: { marginLeft: 'auto' } }),
            React.createElement("span", { style: { paddingBottom: 0, color: 'white' } },
                React.createElement(SettingsControl, { onOpenSettings: onOpenSettings, color: 'white' }),
                React.createElement(ServerStatusControl, { color: 'white' }),
                React.createElement(HitherJobMonitorControl, { onClick: onOpenJobMonitor })))));
};
export default ApplicationBar;
//# sourceMappingURL=ApplicationBar.js.map