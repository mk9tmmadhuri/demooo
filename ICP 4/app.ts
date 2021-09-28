import { Component } from '@angular/core';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'ToDoList';
    items = ['Task 1', 'Task 2', 'Task 3'];
    counter = 0;
    newItem = '';
    valid = false;

    submitNewItem() {
        if (this.newItem !== '') {
            this.items.push(this.newItem); // adding new task only if input value is not empty
            this.newItem = '';
        }
        // @ts-ignore
        document.getElementById('addItem').focus(); //resetting focus back to input field after adding task to list
    }
    completeItem(item: any, i: any) {
        // @ts-ignore
        document.getElementById(i).innerHTML = '<del>'  + item + '</del>'; //striking of task when completed
    }
    deleteItem(i: any) {
        this.items.splice(i,1); //deleting task onclick delete button
    }

}
