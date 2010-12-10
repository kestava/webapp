var itemIdCol = 1,
    itemDescCol = 2,
    detailDescCol = 3,
    effortCol = 4,
    priorityCol = 5,
    sprintsCol = 6,
    statusCol = 7,
    daysCol = 8,
    releaseCol = 9,
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
      _days = values[3],
      _status = values[4];
        
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
}

function SprintBacklog(sprintNum) {
    var files, file, i, tasks = [], row = sprintBacklogStartRow, sheet, range,
        currentItem, values,
        scrumFolder = ScriptProperties.getProperty('scrumFolder');

    this.getSprintNumber = function() { return sprintNum; };

    this.getFilename = function() {
      return 'Sprint ' + sprintNum + ' Backlog';
    };
  
    // Return true if the sprint backlog contains any uncancelled
    // tasks for the given item id
    this.hasItem = function(itemId) {
      var i;
      for (i in tasks) {
        if (tasks.hasOwnProperty(i)) {
          if (tasks[i].getItemId() == itemId) {
            if (!cancelledRe.test(tasks[i].getStatus())) {
              return true;
            }
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
      
      for (i in tasks) {
        if (tasks.hasOwnProperty(i)) {
          task = tasks[i];
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
      return {
        'inProgress': inProgress,
        'done': done,
        'notStarted': notStarted
      };
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
    print('File id: ' + file.getId());
    while (true) {
      sheet = SpreadsheetApp.open(file).getSheetByName('Tasks');
      range = sheet.getRange(row++, 1, 1, 5);
      values = range.getValues();
      currentItem = new SprintTask(range, values[0]);
      
      if (!currentItem.getTaskId()) {
        break;
      }
          
      tasks.push(currentItem);
    }
      
    print('Tasks: ' + tasks.length); 
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
        _itemId = values[0],
        _itemDesc = values[1],
        _detailDesc = values[2],
        _effort = values[3],
        _priority = values[4],
        _release = values[8];
      
    this.getItemId = function() {
        if ('' === _itemId) { return null; }
        return _itemId;
    };
        
    this.updateSprints = function(sprintBacklogs) {
        var cell = _range.getCell(1, sprintsCol),
            i,
            //rev = sprintBacklogs.slice(),
            backlog,
            s = '';
        
      // Use the last sprint backlog to contain uncancelled tasks for the current
      // item id
      //rev.reverse();

      for (i in sprintBacklogs) {
        if (sprintBacklogs.hasOwnProperty(i)) {
          backlog = sprintBacklogs[i];
          if (backlog.hasItem(_itemId)) {
            //cell.setValue(backlog.getSprintNumber());
            //return;
            if (0 < s.length) {
              s += ', ';
            }
            s += backlog.getSprintNumber();
          }
        }
      }
      
      // If what we've got at this point can be interpreted as a number, then
      // we need to prepend an apostrophe so it will display as a string
      //print(s, 's');
      //var blah = Number(s);
      //print(blah, 'blah');
      //cell.setValue(s);
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
    
  this.updateStatus = function(sprintBacklogs) {
    // Examine the status on the backlog item's sprint tasks.
    // If all are 'Not started', return 'Not started'.
    // If all are 'Done', return 'Done'.  
    // If any are 'In progress', return 'In progress'
    var cell = _range.getCell(1, statusCol),
      i,
      backlog,
      statusCounts,
      inProgress = 0,
      done = 0,
      notStarted = 0,
      status = "I'm confused!";
          
    for (i in sprintBacklogs) {
      if (sprintBacklogs.hasOwnProperty(i)) {
        backlog = sprintBacklogs[i];
        statusCounts = backlog.getItemStatus(_itemId);
        inProgress += statusCounts.inProgress;
        done += statusCounts.done;
        notStarted += statusCounts.notStarted;
      }
    }
    
    print('In Progress: ' + inProgress + ', Done: ' + done + ', Not started: ' + notStarted);
    // Figure out the status
    if ((0 == notStarted) && (0 == inProgress) && (0 == done)) {
      status = 'Unassigned';
    }
    else if ((0 < notStarted) && (0 == inProgress) && (0 == done)) {
      status = 'Not started';
    }
    else if ((0 == notStarted) && (0 == inProgress) && (0 < done)) {
      status = 'Done';
    }
    else if ((0 <= notStarted) && (0 < inProgress) && (0 <= done)) {
      status = 'In progress';
    }
    print('Calculated status: ' + status);
    cell.setValue(status);
  };
      
  this.updateDays = function(sprintBacklogs) {
    var cell = _range.getCell(1, daysCol);
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
    currentItem.updateStatus(sprintBacklogs);
    currentItem.updateDays(sprintBacklogs);
  }
}
