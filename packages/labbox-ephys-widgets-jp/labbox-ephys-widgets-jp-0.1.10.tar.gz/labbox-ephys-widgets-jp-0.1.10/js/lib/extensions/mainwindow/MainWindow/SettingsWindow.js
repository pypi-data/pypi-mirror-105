import { Table, TableCell, TableRow } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { LabboxProviderContext } from 'labbox';
import React, { useContext } from 'react';
const useStyles = makeStyles((theme) => ({
    paper: {
        left: 100,
        top: 100,
        right: 100,
        bottom: 100,
        position: 'absolute',
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 4, 3),
        overflow: 'auto'
    },
}));
const SettingsWindow = ({ workspaceUri, version }) => {
    const classes = useStyles();
    const { serverInfo } = useContext(LabboxProviderContext);
    return (React.createElement("div", { className: classes.paper, style: { zIndex: 9999 } },
        React.createElement("h2", null,
            "Labbox Ephys ",
            version),
        React.createElement(Table, null,
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Workspace URI"),
                React.createElement(TableCell, null, workspaceUri || '')),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Kachery node ID"),
                React.createElement(TableCell, null, serverInfo ? serverInfo.nodeId : '')),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Default feed ID"),
                React.createElement(TableCell, null, serverInfo ? serverInfo.defaultFeedId : '')))));
};
export default SettingsWindow;
//# sourceMappingURL=SettingsWindow.js.map