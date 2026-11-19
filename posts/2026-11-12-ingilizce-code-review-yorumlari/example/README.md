# Example: rewriting review comments

The component under review:

```ts
@Component({
  selector: 'app-post-list',
  template: `<li *ngFor="let p of posts">{{ p.title.toUpperCase() }}</li>`,
})
export class PostListComponent implements OnInit {
  posts: any[] = [];
  constructor(private http: HttpClient) {}
  ngOnInit() {
    this.http.get<any[]>('/api/posts').subscribe(r => this.posts = r);
  }
}
```

| # | Bad comment | Better comment |
|---|---|---|
| 1 | "You used any again." | `suggestion:` Could we add a `Post` interface instead of `any[]`? Then the template gets type checking and a typo in `p.title` would fail at build time. |
| 2 | "Memory leak!!" | `issue (non-blocking):` HttpClient completes after one response, so this particular subscribe will not leak. If this ever becomes a long-lived stream, `takeUntilDestroyed()` would be the safe pattern. |
| 3 | "Wrong, use a service." | `question:` Is `/api/posts` used anywhere else? If so, moving the call into a `PostService` would keep the URL in one place. |
| 4 | "Why uppercase in the template?" | `nit:` A CSS `text-transform: uppercase` or a pipe would keep the template free of method calls. Optional. |
| 5 | (nothing) | `praise:` Small and easy to read, thanks! |

Comment 2 is a reminder to check a claim before posting it: HTTP observables complete after one response, so "Memory leak!!" would not only be rude but also wrong.

See [`phrase-bank.md`](phrase-bank.md) for reusable sentences.
