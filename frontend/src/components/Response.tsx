import ReactMarkdown, { type Components } from 'react-markdown'
import remarkGfm from 'remark-gfm'
import '../App.css'

/*
    This component prints out the response of NaviGator
    to the frontend
*/  

// props passed down from the parent (Chat.tsx)
type ResponseProps = {
  response: string
}

function Response({ response }: ResponseProps) {

  // tailwind styling for every Markdown element NaviGator may produce
  const markdownComponents: Components = {
    h1: (props) => (
        <h1 className="text-xl font-bold" {...props} />
    ),
    h2: (props) => (
        <h2 className="text-lg font-bold" {...props} />
    ),
    h3: (props) => (
        <h3 className="text-base font-semibold" {...props} />
    ),
    h4: (props) => (
        <h4 className="text-base font-semibold" {...props} />
    ),
    p: (props) => (
        <p className="leading-relaxed" {...props} />
    ),
    ul: (props) => (
        <ul className="list-disc space-y-1 pl-6" {...props} />
    ),
    ol: (props) => (
        <ol className="list-decimal space-y-1 pl-6" {...props} />
    ),
    a: (props) => (
        <a className="text-indigo-600 underline hover:text-indigo-500" target="_blank" rel="noreferrer" {...props} />
    ),
    blockquote: (props) => (
        <blockquote className="border-l-4 border-gray-300 pl-3 text-gray-600" {...props} />
    ),
    hr: () => (
        <hr className="border-gray-200" />
    ),
    pre: (props) => (
        <pre className="overflow-x-auto rounded-md bg-gray-100 p-3 text-sm" {...props} />
    ),
    code: ({ className, ...props }) => ( 
        <code className={`${className ?? 'rounded bg-gray-100 px-1 py-0.5 text-sm'}`} {...props} />
    ),
    table: (props) => (
        <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm" {...props} />
        </div>
    ),
    thead: (props) => (
        <thead className="bg-gray-50" {...props} />
    ),
    th: (props) => (
        <th className="border border-gray-200 px-3 py-2 text-left font-semibold" {...props} />
    ),
    td: (props) => (
        <td className="border border-gray-200 px-3 py-2 align-top" {...props} />
    ),
  }

  return (
    <>
      <div className="mt-6 flex flex-col items-center">

        {response && (
            <div className="mt-6 w-full max-w-2xl space-y-3 wrap-break-word rounded-md border border-gray-200 bg-white p-4 text-left text-gray-900">
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
                {response}
                </ReactMarkdown>
            </div>
        )}

      </div>
    </>
  )
}

export default Response
