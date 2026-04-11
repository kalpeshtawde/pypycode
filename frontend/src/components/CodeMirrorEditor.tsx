import { useEffect, useRef } from 'react';
import { EditorState } from '@codemirror/state';
import { EditorView, lineNumbers } from '@codemirror/view';
import { python } from '@codemirror/lang-python';
import { vim } from '@replit/codemirror-vim';
import { HighlightStyle, syntaxHighlighting, indentOnInput } from '@codemirror/language';
import { tags as t } from '@lezer/highlight';
import { history, indentMore, indentLess } from '@codemirror/commands';
import { keymap } from '@codemirror/view';
import { indentUnit } from '@codemirror/language';
import { closeBrackets, closeBracketsKeymap } from '@codemirror/autocomplete';

const lightHighlightStyle = HighlightStyle.define([
  { tag: t.keyword, color: '#d73a49' },
  { tag: t.atom, color: '#005cc5' },
  { tag: t.number, color: '#005cc5' },
  { tag: t.string, color: '#032f62' },
  { tag: t.variableName, color: '#24292e' },
  { tag: t.function(t.variableName), color: '#6f42c1' },
  { tag: t.comment, color: '#6a737d' },
  { tag: t.operator, color: '#d73a49' },
]);

interface CodeMirrorEditorProps {
  value: string;
  onChange: (value: string) => void;
  fontSize: number;
  vimMode: boolean;
}

export default function CodeMirrorEditor({
  value,
  onChange,
  fontSize,
  vimMode,
}: CodeMirrorEditorProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<EditorView | null>(null);
  const onChangeRef = useRef(onChange);
  
  // Keep onChange ref up to date without recreating editor
  useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  useEffect(() => {
    if (!containerRef.current) return;

    const extensions: any[] = [
      history(),
      lineNumbers(),
      indentOnInput(),
      closeBrackets(),
      indentUnit.of('    '),
      python(),
      keymap.of([
        ...closeBracketsKeymap,
        { key: 'Tab', run: indentMore },
        { key: 'Shift-Tab', run: indentLess },
      ]),
      EditorView.updateListener.of((update: any) => {
        if (update.docChanged) {
          onChangeRef.current(update.state.doc.toString());
        }
      }),
      syntaxHighlighting(lightHighlightStyle),
      EditorView.theme({
        '.cm-editor': {
          fontFamily: "'JetBrains Mono', monospace",
          height: '100%',
          backgroundColor: '#f8fafc',
          color: '#0f172a',
        },
        '.cm-scroller': {
          overflow: 'auto',
          fontFamily: "'JetBrains Mono', monospace",
        },
        '.cm-gutters': {
          backgroundColor: '#f8fafc',
          borderRight: '1px solid #e2e8f0',
          color: '#64748b',
        },
        '.cm-activeLineGutter': {
          backgroundColor: '#f1f5f9',
        },
        '.cm-cursor': {
          borderLeftColor: '#1a6bff',
        },
        '.cm-content': {
          caretColor: '#1a6bff',
        },
        '.cm-selectionBackground': {
          backgroundColor: '#bfdbfe !important',
        },
        '.cm-focused .cm-selectionBackground': {
          backgroundColor: '#93c5fd !important',
        },
        '&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground': {
          backgroundColor: '#93c5fd',
        },
      }),
    ];

    if (vimMode) {
      extensions.push(vim());
    }

    const state = EditorState.create({
      doc: value,
      extensions,
    });

    if (editorRef.current) {
      editorRef.current.destroy();
    }

    const editor = new EditorView({
      state,
      parent: containerRef.current,
    });

    editorRef.current = editor;

    return () => {
      editor.destroy();
    };
  }, [vimMode]);

  useEffect(() => {
    if (editorRef.current && editorRef.current.state.doc.toString() !== value) {
      editorRef.current.dispatch({
        changes: {
          from: 0,
          to: editorRef.current.state.doc.length,
          insert: value,
        },
      });
    }
  }, [value]);

  useEffect(() => {
    if (editorRef.current && containerRef.current) {
      const editorElement = containerRef.current.querySelector('.cm-editor') as HTMLElement;
      if (editorElement) {
        editorElement.style.fontSize = `${fontSize}px`;
      }
    }
  }, [fontSize]);

  return <div ref={containerRef} style={{ height: '100%', width: '100%' }} />;
}
