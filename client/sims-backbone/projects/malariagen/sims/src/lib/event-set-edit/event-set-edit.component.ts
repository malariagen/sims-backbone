import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';

import { MatDialog } from '@angular/material/dialog';
import { ErrorDialogComponent } from '../error-dialog/error-dialog.component';

import { EventSet } from '../typescript-angular-client/model/eventSet';
import { EventSetNote } from '../typescript-angular-client/model/eventSetNote';
import { EventSetService } from '../typescript-angular-client/api/eventSet.service';

@Component({
  selector: 'sims-event-set-edit',
  providers: [EventSetService],
  templateUrl: './event-set-edit.component.html',
  styleUrls: ['./event-set-edit.component.scss']
})
export class EventSetEditComponent implements OnInit {
  eventSet: EventSet;

  eventSetId: string;

  public eventSetForm: FormGroup;

  constructor(private eventSetService: EventSetService, private route: ActivatedRoute, private _fb: FormBuilder, public dialog: MatDialog) { }

  ngOnInit() {

    this.route.paramMap.subscribe(pmap => this.eventSetId = pmap.get('eventSetId'));

    this.eventSetService.downloadEventSet(this.eventSetId, 0, 0).subscribe(
      (eventSet: EventSet) => {
        this.eventSet = eventSet;

        this.eventSetForm = this._fb.group(
          {
            event_set_name: [this.eventSet.event_set_name, [Validators.required]],
            notes: this._fb.array([]),
          }
        );
        const formIdents = <FormArray>this.eventSetForm.controls['notes'];

        if (this.eventSet.notes) {
          this.eventSet.notes.forEach(note => {
            const noteControl = this.initNoteControl(note);

            formIdents.push(noteControl);
          });
        }
      }
    );
  }

  initNoteControl(note: EventSetNote) {
    let note_name = '';
    let note_text = '';
    if (note) {
      note_name = note.note_name;
      note_text = note.note_text;
    }
    return new FormGroup({
      note_name: new FormControl(note_name, Validators.required),
      note_text: new FormControl(note_text)
    });
  }
  public onSubmit({ value, valid }: { value: EventSet, valid: boolean }): void {

    // console.log("Submitting:" + JSON.stringify(value));
    this.eventSetService.updateEventSet(value.event_set_name, value)
      .subscribe(
        (x) => {
          // console.log("Submitted");
        },
        (e) => {
          // console.log(e);
          const dialogRef = this.dialog.open(ErrorDialogComponent, {
            width: '250px',
            data: { name: 'Error on save', message: e.message }
          });

          dialogRef.afterClosed().subscribe(result => {
            // console.log('The dialog was closed');
          });
        },
        () => {
          // console.log('Completed update.');
        }
      );
  }

  addNote() {
    const notesControl = <FormArray>this.eventSetForm.controls['notes'];
    const newNoteControl = this.initNoteControl(null);
    notesControl.push(newNoteControl);

  }

  removeNote(i: number) {
    const notesControl = <FormArray>this.eventSetForm.controls['notes'];
    notesControl.removeAt(i);
  }

  getNotes() {
    return (<FormArray>(this.eventSetForm.controls['notes'])).controls;
  }
}
