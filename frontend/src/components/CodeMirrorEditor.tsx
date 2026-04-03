import { useEffect, useRef } from 'react';
import { EditorState } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
import { python } from '@codemirror/lang-python';
import { vim } from '@replit/codemirror-vim';

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

  useEffect(() => {
    if (!containerRef.current) return;

    const extensions: any[] = [
      python(),
      EditorView.updateListener.of((update: any) => {
        if (update.docChanged) {
          onChange(update.state.doc.toString());
        }
      }),
      EditorView.theme({
        '.cm-editor': {
          fontSize: `${fontSize}px`,
          fontFamily: "'JetBrains Mono', monospace",
          height: '100%',
          backgroundColor: '#f8fafc',
          color: '#0f172a',
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
  }, [vimMode, onChange]);

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

  return <div ref={containerRef} style={{ height: '100%', width: '100%' }} />;
}
