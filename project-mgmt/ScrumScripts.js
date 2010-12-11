var sprintsCol = 8,
    daysCol = 9,
    sprintBacklogFilenameRe = /^sprint (\d+(.\d+)?) backlog$/i,
    cancelledRe = /^cancelled$/i,
    inProgressRe = /^in progress$/i,
    doneRe = /^done$/i,
    notStartedRe = /^not started$/i,
    productBacklogStartRow = 2,
    sprintBacklogStartRow = 3;

function print(message, context) {
  if (context) {
    Logger.log(context + ': ' + message);
  }
  else {
    Logger.log(message);
  }
}

function compareAsNumeric(l, r) {
  var ln = Number(l), rn = Number(r);
  if (ln < rn) { return -1; }
  else if (ln > rn) { return 1; }
  return 0;
}

function getSprintNumber(file) {
  var match = sprintBacklogFilenameRe.exec(file),
    o = null;
      
  //print(match);
  if (match) {
    o = match[1];
  }
  return o;
}

function getAllSprints() {
  var i, j,
      o = [],
      scrumFolder = ScriptProperties.getProperty('scrumFolder');
      files = DocsList.getFolder(scrumFolder).getFiles();
      
  for (i in files) {
    if (files.hasOwnProperty(i)) {
      j = getSprintNumber(files[i].getName());
      if (j) {
        o.push(j);
      }
    }
  }
  //print(o);
  o.sort(compareAsNumeric);
  print(o, 'Sprints');
  return o;
}

function SprintTask(range, values) {
  var _range = range,
      _taskId = values[0],
      _itemId = values[1],
      _taskDesc = values[2],
      _status = values[3],
      _originalDays = values[4],
      _remainingDays,
      i,
      days;
        
  this.getTaskId = function() {
    if ('' === _taskId) { return null; }
    return _taskId;
  };
  
  this.getItemId = function() {
    return _itemId;
  };
  
  this.getStatus = function() {
    return _status;
  };
  
  this.isCancelled = function() {
    return cancelledRe.test(_status);
  };
    
  this.getOriginalDays = function() {
    return _originalDays;
  };
    
  this.getRemainingDays = function() {
    return _remainingDays;
  };

  if (_taskId) {
    // Get the remaining days. It's found in the last column that has a numeric value.
    //print(_taskId, 'Days for task id');
    for (i = values.length - 1; i > 3; i--) {
      days = parseInt(values[i], 10);
      if (!isNaN(days)) {
        _remainingDays = days;
        break;
      } 
    }
  }
}

function SprintBacklog(sprintNum) {
  var files, file, i, _tasks = [], row = sprintBacklogStartRow, sheet, range,
      task, values,
      scrumFolder = ScriptProperties.getProperty('scrumFolder'),
      lastColumnIdx;

  this.getSprintNumber = function() { return sprintNum; };

  this.getFilename = function() {
    return 'Sprint ' + sprintNum + ' Backlog';
  };
  
  this.getItemDays = function(itemId) {
    var i, currentTask, o = NaN;
    for (i in _tasks) {
      if (_tasks.hasOwnProperty(i)) {
        currentTask = _tasks[i];
        if ((itemId == currentTask.getItemId()) && !currentTask.isCancelled()) {
          o = isNaN(o) ? currentTask.getRemainingDays() : o + currentTask.getRemainingDays();
        }
      }
    }
    return o;
  };
  
  // Return true if the sprint backlog contains any uncancelled
  // tasks for the given item id
  this.hasItem = function(itemId) {
    var i, currentTask;
    for (i in _tasks) {
      if (_tasks.hasOwnProperty(i)) {
        currentTask = _tasks[i];
        if ((currentTask.getItemId() == itemId) && !currentTask.isCancelled()) {
          return true;
        }
      }
    }
    return false;
  };
      
  this.getFile = function() {
    return file;
  };
      
  this.getItemStatus = function(itemId) {
    var i, task,
        inProgress = 0,
        done = 0,
        notStarted = 0;
      
    for (i in _tasks) {
      if (_tasks.hasOwnProperty(i)) {
        task = _tasks[i];
        if (task.getItemId() == itemId) {
          // Ignore any that are "Cancelled"
          if (inProgressRe.test(task.getStatus())) {
            inProgress++;
          }
          else if (doneRe.test(task.getStatus())) {
            done++;
          }
          else if (notStartedRe.test(task.getStatus())) {
            notStarted++;
          }
        }
      }
    }
    return { 'inProgress': inProgress, 'done': done, 'notStarted': notStarted };
  };
      
  files = DocsList.getFolder(scrumFolder).getFiles();  
  for (i in files) {
    if (files.hasOwnProperty(i)) {
      if (this.getFilename() == files[i].getName()) {
        file = files[i];
        break;
      }
    }
  }
          
  // Read the tasks from the file
  print(file.getName(), 'File name'); 
  print(file.getId(), 'File id');
  while (true) {
    sheet = SpreadsheetApp.open(file).getSheetByName('Tasks');
    lastColumnIdx = sheet.getLastColumn();
    print(lastColumnIdx, 'Last column idx');
    range = sheet.getRange(row++, 1, 1, lastColumnIdx);
    values = range.getValues();
    //print(values, 'Task data');
    task = new SprintTask(range, values[0]);
    if (!task.getTaskId()) {
      break;
    }
    print(task.getTaskId(), 'Task id');
    print(task.getOriginalDays(),  'Original days');
    print(task.getRemainingDays(), 'Remaining days');      
    _tasks.push(task);
  }
      
  print(_tasks.length, 'Task count'); 
}
          
function getAllSprintBacklogs() {
  var sprints = getAllSprints(),
      i,
      o = [];
  
  for (i in sprints) {
    if (sprints.hasOwnProperty(i)) {
      o.push(new SprintBacklog(sprints[i]));
    }
  }
  
  return o;
}

function ProductBacklogItem(range, values) {    
    var _range = range,
        _itemId = values[0];
      
    this.getItemId = function() {
        if ('' === _itemId) { return null; }
        return _itemId;
    };
        
  this.updateSprints = function(sprintBacklogs) {
    var cell = _range.getCell(1, sprintsCol),
        i,
        backlog,
        s = '';

    for (i in sprintBacklogs) {
      if (sprintBacklogs.hasOwnProperty(i)) {
        backlog = sprintBacklogs[i];
        if (backlog.hasItem(_itemId)) {
          if (0 < s.length) {
            s += ', ';
          }
          s += backlog.getSprintNumber();
        }
      }
    }
      
    // If what we've got at this point can be interpreted as a number, then
    // we need to prepend an apostrophe so it will display as a string
    if ('' === s) {
      cell.setValue(s);
    }
    else if (isNaN(s)) {
      cell.setValue(s);
    }
    else {
      cell.setValue("'" + s);
    }
  };
      
  this.updateDays = function(sprintBacklogs) {
    // Total the number of days on uncancelled sprint tasks associated
    // with the PBI
    var cell = _range.getCell(1, daysCol), i, backlog, total = NaN, j;
    for (i in sprintBacklogs) {
      if (sprintBacklogs.hasOwnProperty(i)) {
        backlog = sprintBacklogs[i];
        j = backlog.getItemDays(_itemId);
        if (!isNaN(j)) {
          total = isNaN(total) ? j : total + j;
        }
      }
    }
    cell.setValue(isNaN(total) ? '' : total);
  };
}

function updateBacklog() {
  var sprintBacklogs = getAllSprintBacklogs(),
      pbItems = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Items'),
      row = productBacklogStartRow,
      range,
      values,
      currentItem;
    
  while (true) {
    range = pbItems.getRange(row++, 1, 1, 9);
    values = range.getValues();
    currentItem = new ProductBacklogItem(range, values[0]);
      
    if (!currentItem.getItemId()) {
      break;
    }
          
    currentItem.updateSprints(sprintBacklogs);
    currentItem.updateDays(sprintBacklogs);
  }
    
  Browser.msgBox('Finished', Browser.Buttons.OK);
}
