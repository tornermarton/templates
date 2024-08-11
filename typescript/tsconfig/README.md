# TSConfig

Base `tsconfig.json` configurations for TS development.

[Docs](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)

[How to extend](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html#tsconfig-bases)

## Production

For production compilation overwrite the following compilerOptions:
(applications only, libraries should emit all information)
```json
{
  ...
  
  "compilerOptions": {
    ...
    
    "declaration": false,
    "declarationMap": false,
    "sourceMap": false,
    "removeComments": true,
    
    ...
  },
  
  ...
}
```


## JSON modules

```json
{
  ...
  
  "compilerOptions": {
    ...

    "resolveJsonModule": true,
    
    ...
  },
  
  ...
}
```


## Symlinks

```json
{
  ...
  
  "compilerOptions": {
    ...
    
    "preserveSymlinks": true,
    
    ...
  },
  
  ...
}
```


## Decorators

Using:
```json
{
  ...
  
  "compilerOptions": {
    ...
    
    "experimentalDecorators": true,
    
    ...
  },
  
  ...
}
```

Providing:
```json
{
  ...
  
  "compilerOptions": {
    ...,

    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    
    ...
  },
  
  ...
}
```
